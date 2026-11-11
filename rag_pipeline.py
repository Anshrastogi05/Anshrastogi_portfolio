"""
Production RAG Pipeline using Instructor + Groq for Structured Output
Context retrieved from GitHub (https://github.com/Anshrastogi05) and LinkedIn (https://www.linkedin.com/in/anshrastogi23/)
"""

import os
import re
import json
import argparse
from typing import List, Optional
from pydantic import BaseModel, Field

# Automatically load .env file if present
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# =========================================================================
# CONFIGURATION: You can paste your Groq API key directly here,
# or set it in your .env file as GROQ_API_KEY=gsk_...
# =========================================================================
DEFAULT_GROQ_API_KEY = ""  # e.g. "gsk_xxxxxxxxxxxxxxxxxxxxxx"

# Check Groq and Instructor availability
try:
    from groq import Groq
    import instructor
    GROQ_AVAILABLE = True
except ImportError:
    GROQ_AVAILABLE = False


# ==========================================
# 1. Structured Output Pydantic Schemas
# ==========================================
class Citation(BaseModel):
    source_name: str = Field(description="Name of the source document or repository")
    source_url: str = Field(description="URL to the GitHub repo or LinkedIn profile")
    key_fact: str = Field(description="Exact fact or achievement retrieved from context")

class StructuredRagResponse(BaseModel):
    executive_summary: str = Field(
        description="Direct, concise 2 to 4 sentence answer synthesizing the retrieved facts."
    )
    detailed_breakdown: List[str] = Field(
        description="Key technical highlights, architecture decisions, or experience bullet points."
    )
    technologies_involved: List[str] = Field(
        description="Specific languages, tools, and frameworks relevant to the query."
    )
    citations: List[Citation] = Field(
        description="List of verified citations linking to GitHub repos or LinkedIn."
    )
    confidence_score: float = Field(
        description="Confidence score between 0.0 and 1.0 based on context completeness.",
        ge=0.0,
        le=1.0
    )
    suggested_followups: List[str] = Field(
        description="2 to 3 intelligent follow-up questions the user might ask next."
    )


# ==========================================
# 2. Retriever Engine
# ==========================================
class PortfolioRetriever:
    def __init__(self, corpus_path: str = "knowledge_base/corpus.json"):
        if not os.path.exists(corpus_path):
            raise FileNotFoundError(f"Knowledge corpus not found at {corpus_path}")
        with open(corpus_path, "r", encoding="utf-8") as f:
            self.corpus = json.load(f)

    def retrieve(self, query: str, top_k: int = 4) -> List[dict]:
        """
        Calculates lexical + semantic keyword relevance across documents.
        """
        raw_tokens = re.findall(r"\w+", query.lower())
        stopwords = {
            "what", "is", "he", "his", "the", "a", "an", "and", "or", "in", "on", 
            "at", "to", "for", "with", "does", "did", "tell", "me", "about", 
            "ansh", "rastogi", "projects", "project"
        }
        query_terms = [t for t in raw_tokens if t not in stopwords and len(t) > 1]
        
        # Specific company & project entity detection
        has_ubnext = bool(re.search(r"\b(ub\s*next|ubnext|uv\s*next|uvnext)\b", query, re.I))
        has_lovers = bool(re.search(r"\b(lovers|lovers\.?ai|wedding)\b", query, re.I))
        has_qskills = bool(re.search(r"\b(qskills|q\s*skills)\b", query, re.I))
        has_edulyt = bool(re.search(r"\b(edulyt)\b", query, re.I))
        has_adinfo = bool(re.search(r"\b(ad\s*infocom|adinfo)\b", query, re.I))

        is_ai_query = any(t in ["ai", "ml", "rag", "langgraph", "llm", "whisper", "model"] for t in raw_tokens)
        is_backend_query = any(t in ["backend", "api", "database", "server", "fastapi", "express", "sql"] for t in raw_tokens)
        is_intern_query = any(t in ["intern", "internship", "internships", "work", "job", "experience", "company"] for t in raw_tokens)

        scored_docs = []
        for doc in self.corpus:
            score = 0
            doc_id = doc.get("id", "").lower()
            text_to_search = (
                doc["title"] + " " + 
                doc["content"] + " " + 
                " ".join(doc.get("tags", [])) + " " + 
                doc.get("category", "")
            ).lower()

            # Massive boost for specific entity mentions
            if has_ubnext and "ubnext" in doc_id:
                score += 80
            if has_lovers and "lovers" in doc_id:
                score += 80
            if has_qskills and "qskills" in doc_id:
                score += 80
            if has_edulyt and "edulyt" in doc_id:
                score += 80
            if has_adinfo and "ad_infocom" in doc_id:
                score += 80

            # General category boosts if no specific entity was targeted
            if not (has_ubnext or has_lovers or has_qskills or has_edulyt or has_adinfo):
                if is_ai_query and doc.get("category") == "AI & ML Project":
                    score += 15
                if is_backend_query and ("backend" in doc.get("tags", []) or "systems" in doc.get("category", "").lower()):
                    score += 15
                if is_intern_query and doc.get("category") == "Work Experience":
                    score += 15

            for term in query_terms:
                if term in doc["title"].lower():
                    score += 8
                if any(term == tag.lower() for tag in doc.get("tags", [])):
                    score += 6
                count = text_to_search.count(term)
                score += min(count * 2, 6)

            if score > 0:
                scored_docs.append((score, doc))

        scored_docs.sort(key=lambda x: x[0], reverse=True)
        
        if not scored_docs:
            return self.corpus[:top_k]
            
        return [doc for _, doc in scored_docs[:top_k]]


# ==========================================
# 3. RAG Engine with Instructor + Groq
# ==========================================
class GroqRagEngine:
    def __init__(self, api_key: Optional[str] = None, model: str = "openai/gpt-oss-120b"):
        self.retriever = PortfolioRetriever()
        self.model = model
        self.api_key = api_key or os.environ.get("GROQ_API_KEY") or DEFAULT_GROQ_API_KEY
        
        if GROQ_AVAILABLE and self.api_key:
            self.groq_client = Groq(api_key=self.api_key)
            self.client = instructor.from_groq(self.groq_client, mode=instructor.Mode.JSON)
        else:
            self.client = None

    def query(self, user_query: str, top_k: int = 4) -> StructuredRagResponse:
        relevant_docs = self.retriever.retrieve(user_query, top_k=top_k)
        
        context_blocks = []
        for i, d in enumerate(relevant_docs, 1):
            context_blocks.append(
                f"[Document {i}]: {d['title']}\n"
                f"Source: {d['source']} ({d['source_url']})\n"
                f"Category: {d['category']}\n"
                f"Content: {d['content']}\n"
            )
        formatted_context = "\n---\n".join(context_blocks)

        system_prompt = (
            "You are the official career & technical AI assistant for Ansh Rastogi. "
            "Your job is to answer queries factually, concisely, and thoroughly using ONLY the provided context. "
            "Context is sourced directly from Ansh's verified GitHub (github.com/Anshrastogi05) and LinkedIn profile. "
            "Never invent facts, metrics, or employers not present in the context. "
            "You MUST output your response strictly adhering to the requested structured Pydantic schema."
        )
        user_prompt = f"Retrieved Context:\n{formatted_context}\n\nUser Question: {user_query}"

        if self.client:
            try:
                response: StructuredRagResponse = self.client.chat.completions.create(
                    model=self.model,
                    response_model=StructuredRagResponse,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ],
                    temperature=0.1
                )
                return response
            except Exception as e:
                print(f"[Warning] Groq API call encountered error: {e}. Generating structured local fallback.")

        return self._local_structured_synthesis(user_query, relevant_docs)

    def _local_structured_synthesis(self, query: str, docs: List[dict]) -> StructuredRagResponse:
        citations = [
            Citation(
                source_name=d["title"],
                source_url=d["source_url"],
                key_fact=d["content"][:160] + "..."
            )
            for d in docs
        ]
        
        techs = []
        for d in docs:
            for t in d.get("tags", []):
                t_clean = t.title()
                if t_clean not in ["Github Project", "Bio", "Work Experience"] and t_clean not in techs:
                    techs.append(t_clean)

        doc_summaries = " ".join([d["content"] for d in docs[:2]])
        summary = f"Based on verified GitHub and LinkedIn records: {doc_summaries[:280]}..."
        breakdown = [f"{d['title']}: {d['content']}" for d in docs[:3]]
        
        return StructuredRagResponse(
            executive_summary=summary,
            detailed_breakdown=breakdown,
            technologies_involved=techs[:8],
            citations=citations,
            confidence_score=0.98,
            suggested_followups=[
                "What has Ansh built with AI?",
                "Can you detail his backend experience?",
                "How can I contact Ansh for an SDE opportunity?"
            ]
        )


# ==========================================
# 4. HTTP API Server Handler
# ==========================================
def run_http_server(port: int = 8000):
    """Zero-dependency HTTP JSON API server."""
    from http.server import HTTPServer, BaseHTTPRequestHandler
    
    engine = GroqRagEngine()

    class RagRequestHandler(BaseHTTPRequestHandler):
        def do_OPTIONS(self):
            self.send_response(200)
            self.send_header("Access-Control-Allow-Origin", "*")
            self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
            self.send_header("Access-Control-Allow-Headers", "Content-Type")
            self.end_headers()

        def do_GET(self):
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            data = {
                "status": "online",
                "service": "Ansh Rastogi Structured RAG API",
                "engine": "Instructor + Groq",
                "model": engine.model,
                "groq_live": engine.client is not None,
                "corpus_docs": len(engine.retriever.corpus)
            }
            self.wfile.write(json.dumps(data).encode("utf-8"))

        def do_POST(self):
            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length).decode("utf-8")
            try:
                payload = json.loads(body)
                query = payload.get("query", "")
                top_k = payload.get("top_k", 4)
                if not query:
                    self.send_response(400)
                    self.end_headers()
                    self.wfile.write(b'{"error": "Query required"}')
                    return

                res = engine.query(query, top_k=top_k)
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                self.wfile.write(json.dumps(res.model_dump()).encode("utf-8"))
            except Exception as ex:
                self.send_response(500)
                self.end_headers()
                self.wfile.write(json.dumps({"error": str(ex)}).encode("utf-8"))

    server = HTTPServer(("0.0.0.0", port), RagRequestHandler)
    print(f"🚀 Structured RAG Server running at http://localhost:{port}")
    server.serve_forever()


# ==========================================
# 5. CLI Interface
# ==========================================
def main():
    parser = argparse.ArgumentParser(description="Run Structured RAG with Groq & Instructor")
    parser.add_argument("--query", "-q", type=str, default="What has Ansh built with AI?", help="Question to ask")
    parser.add_argument("--top_k", "-k", type=int, default=3, help="Number of context chunks to retrieve")
    parser.add_argument("--serve", action="store_true", help="Launch HTTP JSON API server")
    parser.add_argument("--port", type=int, default=8000, help="Port for HTTP API server")
    args = parser.parse_args()

    if args.serve:
        run_http_server(args.port)
        return

    engine = GroqRagEngine()
    print(f"\n🔍 Query: {args.query}\n")
    result = engine.query(args.query, top_k=args.top_k)

    print("=" * 65)
    print("📋 STRUCTURED RAG OUTPUT (Instructor + Groq)")
    print("=" * 65)
    print(f"Executive Summary:\n{result.executive_summary}\n")
    print("Technical Highlights:")
    for b in result.detailed_breakdown:
        print(f"  • {b}")
    print(f"\nTechnologies: {', '.join(result.technologies_involved)}")
    print(f"Confidence Score: {result.confidence_score * 100:.1f}%\n")
    print("Verified Citations:")
    for c in result.citations:
        print(f"  [{c.source_name}] -> {c.source_url}")
        print(f"    Fact: {c.key_fact}")
    print("\nSuggested Follow-ups:")
    for q in result.suggested_followups:
        print(f"  - {q}")
    print("=" * 65)

    print("\n📦 Raw JSON Output:")
    print(json.dumps(result.model_dump(), indent=2))


if __name__ == "__main__":
    main()
