# Ansh Rastogi — Engineering Portfolio

[![Live Site](https://img.shields.io/badge/Live-Portfolio-22c55e?style=for-the-badge&logo=googlechrome&logoColor=white)](https://anshrastogi05.github.io/Anshrastogi_portfolio/)
[![Resume](https://img.shields.io/badge/Resume-PDF-blue?style=for-the-badge&logo=adobeacrobatreader&logoColor=white)](Ansh_Rastogi_Resume.pdf)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://linkedin.com/in/anshrastogi23)
[![GitHub](https://img.shields.io/badge/GitHub-Profile-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/Anshrastogi05)

A modern, developer-first personal engineering portfolio built with vanilla web standards, interactive 3D WebGL visualizations, a keyboard-driven command palette, interactive 3D flip cards, a stealth organic honeycomb gallery, and a verified AI-powered conversational assistant (**Ask AshR**) powered by a **Structured RAG pipeline (Pydantic + Instructor + Groq)**.

---

## ✨ Key Features & Architecture

### 🌐 3D Interactive WebGL Network Sphere
* Custom procedural particle sphere engineered with Three.js WebGL.
* Dynamic rotational physics responding to mouse and touch telemetry.
* Zero-bloat, lazy-loaded initialization that never blocks first paint (60 FPS).

### 🤖 "Ask AshR" — Structured RAG AI Assistant
* **Corpus-Grounded Intelligence:** Built on a verified knowledge base (`knowledge_base/corpus.json`) curated directly from GitHub repositories and LinkedIn work records.
* **Pydantic Validation (`rag_pipeline.py`):** Uses strict Pydantic schemas (`StructuredRagResponse`, `Citation`) to eliminate hallucination, guarantee structured output, and provide exact source attribution.
* **Instructor + Groq LLM:** Leverages the `instructor` library with high-throughput Groq models (`openai/gpt-oss-120b`, Llama 3) for sub-second structured inference.
* **Smart Hybrid Architecture:** Queries the live Python RAG server when online (`http://localhost:8000/api/ask`), and seamlessly falls back to a fast client-side keyword engine when deployed as a static site.
* **Dynamic Follow-Up Prompts:** Automatically generates context-aware follow-up chips after every answer.

### 🐝 Stealth Organic Beehive / Honeycomb (About Me)
* **Zero Container / Pure Stealth:** Looks completely natural and empty when idle—no container box, borders, or text overlays.
* **Organic Hexagonal Bloom:** Hovering or moving the cursor across the space triggers an interlocking 6-cell geometric honeycomb bloom featuring verified leadership and event moments from NIT Jalandhar.
* **Tessellated Geometry:** Precise 30°/60° regular hexagonal nesting with amber-emerald edge highlights on focus.

### 🪪 3D Flip Leadership Passes
* Conference VIP badge aesthetic complete with lanyard ribbon, swing physics, hole punch, and barcode detailing.
* **Interactive 3D Card Flip:** Clicking any card smoothly rotates 180° in 3D perspective to reveal the official leadership posters on the backside:
  1. **STRATABIZ Club** (President · Led ConsultCorp with 300+ attendees) ➔ Official President poster
  2. **Bawre Theatre Society** (Operational Director · Stage & production ops) ➔ Official Director poster
  3. **Institution's Innovation Council (IIC)** (Social Media Head · Digital outreach) ➔ Official Head poster

### 🗂️ Interactive Project Architecture Cards
* **Front:** Visual project cards with live demo links, repository buttons, and interactive tech tags.
* **Back (3D Flip):** Clean, spacious technical breakdown highlighting system architecture, latency targets, and engineering decisions.
* **Tech Stack Inspector:** Clicking any skill tag opens an interactive details modal displaying official tech logos, production context, and a 1-click shortcut to ask the AI assistant about that technology.

### ⌨️ Developer-First Ergonomics
* **Raycast-Style Command Palette (`Ctrl + K` / `Cmd + K`):** Instant keyboard navigation across sections, terminal, games, and resume download.
* **Interactive Terminal CLI:** Built-in bash-like shell supporting `about`, `projects`, `experience`, `skills`, `leadership`, `contact`, and `sudo`.
* **Playable Mini-Game:** Interactive Tic-Tac-Toe with minimax logic.

### 📅 Seamless 1-Click Scheduling
* **Cal.com 1-Click Booking:** Directly book real-time Google Meet appointment slots without email back-and-forth.
* **Direct Proposal Modal:** Clean fallback form to send project proposals directly to email.

---

## 🛠️ Tech Stack

| Domain | Technologies |
| :--- | :--- |
| **Frontend** | HTML5, Modern CSS3 (Glassmorphism, CSS Custom Properties, 3D Transforms), Vanilla JavaScript (ES6+), Three.js (WebGL) |
| **AI / RAG Pipeline** | Python 3, **Pydantic v2** (`BaseModel`, `Field`), **Instructor**, **Groq SDK** (`gpt-oss-120b`), Custom Retrieval Engine |
| **Assets & Styling** | Devicon SVGs, Custom Club Emblems, Responsive Grid / Flexbox |
| **Hosting & CI/CD** | GitHub Pages, Vercel, Netlify |

---

## 📁 Project Directory Structure

```text
Ansh_portfolio/
├── assets/                  # Consolidated local images & documents (.gitignored)
│   ├── ansh.jpg             # Profile avatar
│   ├── stratabiz.jpg        # Club logos
│   ├── bawre.jpg
│   ├── iic.jpg
│   ├── lead_stratabiz.jpg   # Official leadership posters (card backsides)
│   ├── lead_bawre.jpg
│   ├── lead_iic.jpg
│   ├── team_1.jpg ... team_6.jpg # Beehive honeycomb event photos
│   └── resume.pdf
├── knowledge_base/          # Verified portfolio knowledge corpus
│   └── corpus.json
├── index.html               # Main single-page portfolio application
├── rag_pipeline.py          # Production RAG pipeline (Pydantic + Instructor + Groq)
├── Ansh_Rastogi_Resume.pdf  # Downloadable PDF resume
├── .env.example             # Example environment configuration
├── .gitignore               # Ignored files, virtual environments, and media assets
└── README.md                # Project documentation
```

---

## 🚀 Running Locally

### 1. Clone the repository
```bash
git clone https://github.com/Anshrastogi05/Anshrastogi_portfolio.git
cd Anshrastogi_portfolio
```

### 2. Launch Frontend (Choose any method)

* **Python HTTP Server (Fastest):**
  ```bash
  python -m http.server 3000
  ```
  Visit: **`http://localhost:3000`**

* **VS Code Live Server:**
  Right-click `index.html` → Select **"Open with Live Server"**.

* **Node.js (`npx`):**
  ```bash
  npx serve .
  ```

---

## 🧠 Running the Pydantic RAG Backend (Optional)

To enable the live Groq-powered AI pipeline for the chatbot:

### 1. Set up Python environment
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

### 2. Install dependencies
```bash
pip install pydantic instructor groq python-dotenv
```

### 3. Configure API Key
Create a `.env` file in the project root:
```env
GROQ_API_KEY=gsk_your_groq_api_key_here
```
*(Get a free high-speed API key at [console.groq.com](https://console.groq.com/))*

### 4. Run the server or CLI

* **Run as HTTP Server for the web portfolio:**
  ```bash
  python rag_pipeline.py --serve --port 8000
  ```
  *The portfolio chatbot will automatically route live queries through `http://localhost:8000/api/ask`.*

* **Test queries directly in your terminal:**
  ```bash
  python rag_pipeline.py -q "What has Ansh built with AI?"
  ```

---

## 📬 Contact & Connect

* **Email:** [rastogiansh13@gmail.com](mailto:rastogiansh13@gmail.com)
* **LinkedIn:** [linkedin.com/in/anshrastogi23](https://linkedin.com/in/anshrastogi23)
* **GitHub:** [github.com/Anshrastogi05](https://github.com/Anshrastogi05)
* **Schedule a 1-to-1:** [Cal.com Appointment](https://cal.com/ansh-rastogi-qeqqay/30min)

---

<p align="center">
  Designed &amp; Engineered by <b>Ansh Rastogi</b> · Crafted with speed, precision, and clean code.
</p>
