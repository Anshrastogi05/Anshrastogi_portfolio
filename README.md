# Ansh Rastogi — Engineering Portfolio

[![Live Site](https://img.shields.io/badge/Live-Portfolio-22c55e?style=for-the-badge&logo=googlechrome&logoColor=white)](https://anshrastogi05.github.io/Anshrastogi_portfolio/)
[![Resume](https://img.shields.io/badge/Resume-PDF-blue?style=for-the-badge&logo=adobeacrobatreader&logoColor=white)](Ansh_Rastogi_Resume.pdf)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://linkedin.com/in/anshrastogi23)
[![GitHub](https://img.shields.io/badge/GitHub-Profile-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/Anshrastogi05)

A high-performance, developer-first personal portfolio engineered with vanilla web standards, interactive 3D WebGL visualizations, a keyboard-driven command palette, and an AI-powered conversational assistant (**Ask AshR**).

---

## ✨ Key Features & Architecture

### 🌐 3D Interactive WebGL Network Sphere
* Custom particle globe with dynamic rotational physics and mouse/touch telemetry.
* Zero external bloat—smooth 60 FPS canvas rendering without blocking the critical render path.

### 🤖 "Ask AshR" — AI Knowledge Engine & RAG Assistant
* Conversational AI assistant grounded in verified technical background, internships, and project repositories.
* Features fast keyword matching with dynamic follow-up suggestions, plus an optional FastAPI + Groq RAG pipeline (`rag_pipeline.py`).

### ⌨️ Developer-First Ergonomics
* **Raycast-Style Command Palette (`Ctrl + K` / `Cmd + K`):** Instant keyboard navigation across sections, terminal, games, and resume downloads.
* **Interactive Terminal CLI:** Built-in shell supporting commands like `about`, `projects`, `experience`, `skills`, `leadership`, `contact`, and `sudo`.
* **Playable Mini-Game:** Interactive Tic-Tac-Toe with minimax logic.

### 🏷️ Interactive Tech Stack & Popouts
* Detailed tech pill directory featuring official SVG devicons.
* Interactive details modal revealing production use-cases, architecture notes, and instant *"Ask AshR"* prompt shortcuts.

### 🪪 Tactile Leadership Passes
* Physical conference VIP lanyard pass styling with CSS swinging animation, hole punch, barcode strips, and official NIT Jalandhar club emblems:
  * **StrataBiz Club** (President · Led ConsultCorp with 300+ attendees)
  * **Institution's Innovation Council** (Social Media Head · Digital outreach)
  * **Bawre Theatre Society** (Operational Director · Stage & production logistics)

### 📅 Seamless 1-Click Scheduling & Contact
* **Cal.com 1-Click Booking:** Instant Google Meet appointment scheduling via live calendar slots.
* **Direct Custom Request Modal:** Fallback form for custom meeting proposals.
* **Instant Inbox Messaging:** Integrated AJAX form delivering directly to email with real-time validation.

---

## 🛠️ Tech Stack

* **Frontend:** HTML5, Modern CSS3 (Glassmorphism, CSS Variables, 3D Transforms), Vanilla JavaScript (ES6+), Three.js / Canvas WebGL
* **AI / Backend (Optional):** Python 3, FastAPI, Groq SDK, LangChain, ChromaDB / Qdrant, RAG Architecture
* **Icons & Assets:** Devicon SVGs, Custom Club Emblems, Optimized Typography
* **Deployment:** Vercel / GitHub Pages

---

## 🚀 Running Locally

Clone the repository:
```bash
git clone https://github.com/Anshrastogi05/Anshrastogi_portfolio.git
cd Anshrastogi_portfolio
```

### Option 1: Python Built-in Server (Fastest)
```bash
python -m http.server 3000
```
Open your browser and visit: **`http://localhost:3000`**

### Option 2: VS Code Live Server
1. Open the project in VS Code / IDE.
2. Right-click `index.html` → **"Open with Live Server"**.

### Option 3: Node.js `serve` / `npx`
```bash
npx serve .
```

---

## 🧠 (Optional) Running the Local RAG Backend

To power the AI chatbot with the local FastAPI + Groq pipeline:

1. Create a virtual environment and install dependencies:
   ```bash
   python -m venv venv
   source venv/bin/activate   # On Windows: venv\Scripts\activate
   pip install fastapi uvicorn groq chromadb langchain pydantic
   ```
2. Configure `.env`:
   ```env
   GROQ_API_KEY=your_groq_api_key_here
   ```
3. Start the backend:
   ```bash
   python rag_pipeline.py
   ```
   *The portfolio will automatically route live queries through `http://localhost:8000/api/ask`.*

---

## 🚢 Deployment

### Deploy to Vercel (Recommended)
1. Push your repository to GitHub.
2. Sign in to [Vercel](https://vercel.com) and click **"Add New..." → "Project"**.
3. Import `Anshrastogi_portfolio` and click **Deploy**.

### Deploy to GitHub Pages
1. Go to your repository on GitHub → **Settings** → **Pages**.
2. Set **Source** to `Deploy from a branch` → Select `main` and `/(root)`.
3. Click **Save**. Your site will be live at `https://<username>.github.io/<repo>/`.

---

## 📬 Contact & Connect

* **Email:** [rastogiansh13@gmail.com](mailto:rastogiansh13@gmail.com)
* **LinkedIn:** [linkedin.com/in/anshrastogi23](https://linkedin.com/in/anshrastogi23)
* **GitHub:** [github.com/Anshrastogi05](https://github.com/Anshrastogi05)
* **Schedule a 1-to-1:** [Cal.com (Google Meet)](https://cal.com/ansh-rastogi-qeqqay/30min)

---

<p align="center">
  Designed &amp; Engineered by <b>Ansh Rastogi</b> · Built with speed, precision, and clean code.
</p>
