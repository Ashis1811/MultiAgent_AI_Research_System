# 🔬 ResearchMind — Multi-Agent AI Research System

<div align="center">

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![LangChain](https://img.shields.io/badge/LangChain-1C3C3C?style=for-the-badge&logo=langchain&logoColor=white)
![OpenAI](https://img.shields.io/badge/OpenAI-412991?style=for-the-badge&logo=openai&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

**Four specialized AI agents collaborate in real time to deliver polished, verified research reports on any topic.**

[Live Demo](https://multiagentairesearchsystem-dgpajdfqybirappeesi5qhs.streamlit.app/) · [Report Bug](https://github.com/Ashis1811/MultiAgent_AI_Research_System/issues/new?template=bug_report.md) · [Request Feature](https://github.com/Ashis1811/MultiAgent_AI_Research_System/issues/new?template=feature_request.md)

</div>

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Architecture](#-architecture)
- [Step-by-Step Build Process](#-step-by-step-build-process)
- [Project Structure](#-project-structure)
- [Installation](#-installation)
- [Configuration](#-configuration)
- [Usage](#-usage)
- [Deployment](#-deployment)
- [Screenshots](#-screenshots)

---

## 🧠 Overview

ResearchMind is a production-grade **multi-agent AI system** built with LangChain and Streamlit. It orchestrates four specialized AI agents in a sequential pipeline — a Search Agent, a Reader Agent, a Writer Chain, and a Critic Chain — to autonomously research any topic and produce a structured, self-reviewed report.

It also supports a **Document Mode (RAG)** where users can upload PDFs, images, or text files and ask questions directly about their content using Retrieval-Augmented Generation.

---

## ✨ Features

- 🔍 **Search Agent** — Uses Tavily API to find recent, reliable web sources
- 📄 **Reader Agent** — Scrapes and extracts deep content from top URLs
- ✍️ **Writer Chain** — Synthesizes gathered research into a structured report
- 🧐 **Critic Chain** — Reviews and scores the report (quality, accuracy, completeness)
- 📎 **Document Upload (RAG)** — Upload PDFs, images, TXT, CSV, or Markdown files
- 🧬 **Vector Search** — ChromaDB-powered semantic retrieval over uploaded documents
- ⬇️ **Download Reports** — Export final reports as `.md` files
- 🎨 **Premium Dark UI** — Sci-fi editorial design with animated pipeline status cards

---

## 🛠 Tech Stack

| Layer | Technology | Purpose |
|---|---|---|
| **Frontend** | Streamlit | Web UI and session state management |
| **LLM** | GPT-4o-mini via OpenRouter | Powers all agents and chains |
| **Agent Framework** | LangChain | Agent orchestration and tool use |
| **Web Search** | Tavily API | Real-time web search for the Search Agent |
| **Web Scraping** | BeautifulSoup4 + Requests | URL scraping for the Reader Agent |
| **RAG / Embeddings** | ChromaDB + OpenAI text-embedding-3-small | Vector store for document mode |
| **PDF Extraction** | PyMuPDF (fitz) / pdfplumber | Text extraction from PDF uploads |
| **OCR** | pytesseract + Pillow | Text extraction from image uploads |
| **Environment** | python-dotenv | API key management |
| **Styling** | Custom CSS (Bebas Neue, Outfit, JetBrains Mono) | Premium dark UI design |

---

## 🏗 Architecture

```
User Input (Topic or File Upload)
          │
          ▼
┌─────────────────────────────────────────┐
│           ResearchMind Pipeline          │
│                                         │
│  ┌─────────────┐    ┌───────────────┐   │
│  │ Search Agent│───▶│ Reader Agent  │   │
│  │  (Tavily)   │    │ (BeautifulSoup│   │
│  └─────────────┘    └───────┬───────┘   │
│                             │           │
│                    ┌────────▼────────┐  │
│                    │  Writer Chain   │  │
│                    │   (GPT-4o-mini) │  │
│                    └────────┬────────┘  │
│                             │           │
│                    ┌────────▼────────┐  │
│                    │  Critic Chain   │  │
│                    │  (Score /10)    │  │
│                    └─────────────────┘  │
└─────────────────────────────────────────┘
          │
          ▼
   Final Research Report (.md)

─── Document Mode (RAG) ───────────────────
File Upload → Text Extraction → ChromaDB
           → Semantic Retrieval → RAG Chain
           → Answer + Report
```

---

## 🪜 Step-by-Step Build Process

### Step 1 — Project Setup

Created the base project structure and virtual environment.

```bash
mkdir "Multi Agent"
cd "Multi Agent"
python -m venv .venv
.venv\Scripts\activate       # Windows
pip install streamlit langchain langchain-openai tavily-python
```

### Step 2 — Define the Tools (`tools.py`)

Built two core LangChain tools:

- `web_search` — wraps the Tavily API to retrieve recent web results with titles, URLs, and snippets
- `scrape_url` — uses `requests` + `BeautifulSoup` to scrape and clean the text content of a URL

```python
@tool
def web_search(query: str, max_results: int = 5) -> str:
    """Search the web for recent and reliable information."""
    ...

@tool
def scrape_url(url: str) -> str:
    """Scrape and return clean text content from a given URL."""
    ...
```

### Step 3 — Build the Agents and Chains (`agents.py`)

Created four components of the pipeline:

**Search Agent** — A LangChain SimpleAgent equipped with the `web_search` tool. Given a topic, it searches and returns structured results.

**Reader Agent** — A LangChain SimpleAgent equipped with the `scrape_url` tool. It picks the most relevant URL from search results and extracts deep content.

**Writer Chain** — A simple `prompt | llm | StrOutputParser` chain. Takes the combined research (search results + scraped content) and writes a structured report with Introduction, Key Findings, Conclusion, and Sources.

**Critic Chain** — Another prompt chain. Reviews the report and returns a `Score: X/10` with Strengths, Areas to Improve, and a one-line verdict.

**RAG Chain** — For document mode. Takes a question and retrieved context chunks and generates a focused answer.

```python
writer_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an expert research writer..."),
    ("human", "Write a report on: {topic}\n\nResearch:\n{research}"),
])
writer_chain = writer_prompt | llm | StrOutputParser()
```

### Step 4 — Build the RAG System (`rag.py`)

Added Retrieval-Augmented Generation for document uploads:

- `create_vector_store(text)` — splits the document into chunks using `RecursiveCharacterTextSplitter`, embeds them with OpenAI embeddings, and stores in a ChromaDB vector store
- `retrieve_relevant_context(vectorstore, query)` — retrieves the top-k most semantically similar chunks to the user's question

```python
def create_vector_store(text: str):
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = splitter.create_documents([text])
    return Chroma.from_documents(chunks, embeddings)
```

### Step 5 — Build the CLI Pipeline (`pipeline.py`)

Before building the UI, validated the full pipeline end-to-end in the terminal:

```bash
python pipeline.py
# Enter a research topic: LLM agents 2025
```

This confirmed all four agents worked correctly in sequence and output clean results.

### Step 6 — Build the Streamlit UI (`app.py`)

Built the initial Streamlit interface with:

- Left column: topic input + run button
- Right column: animated pipeline status cards (Waiting → Running → Done)
- Results section: raw expanders + final report + critic feedback
- Download button for `.md` export

### Step 7 — Add File Upload Support

Extended the input card with `st.file_uploader` and added three extraction functions to `tools.py`:

- `extract_text_from_pdf()` — PyMuPDF with pdfplumber fallback
- `extract_text_from_image()` — pytesseract OCR via Pillow
- `extract_text_from_txt()` — plain UTF-8 decode
- `extract_file_content()` — universal dispatcher by file extension

When a file is uploaded, the Search and Reader agents are **skipped** and the extracted text goes directly into the Writer via the RAG chain.

### Step 8 — Premium UI Redesign

Replaced the original CSS with a full **sci-fi editorial dark theme**:

- **Fonts**: Bebas Neue (display) + Outfit (body) + JetBrains Mono (labels)
- **Colors**: `#00e5ff` cyan + `#7b61ff` purple + `#ff4d6d` red on `#05050a` base
- **Effects**: scanning animation on active pipeline steps, gradient shimmer on input card top edge, animated file badge dot, gradient hero title with ghost text stroke
- **Components**: top nav bar, hero stats row, status indicator pill, score block with dynamic color

---

## 📁 Project Structure

```
Multi Agent/
│
├── app.py              # Main Streamlit UI — pipeline orchestration + all rendering
├── agents.py           # LangChain agents, writer chain, critic chain, RAG chain
├── tools.py            # web_search, scrape_url, file extraction functions
├── rag.py              # ChromaDB vector store creation and context retrieval
├── pipeline.py         # CLI version for local testing without UI
│
├── requirements.txt    # Python dependencies
├── packages.txt        # System packages for Streamlit Cloud (tesseract-ocr)
├── .env                # API keys (never commit this)
├── .gitignore
└── README.md
```

---

## ⚙️ Installation

### Prerequisites

- Python 3.10+
- Git
- Tesseract OCR (for image uploads)
  - Windows: [Download installer](https://github.com/UB-Mannheim/tesseract/wiki)
  - Ubuntu: `sudo apt install tesseract-ocr`
  - Mac: `brew install tesseract`

### Clone and install

```bash
git clone https://github.com/YOUR_USERNAME/researchmind.git
cd researchmind

python -m venv .venv
.venv\Scripts\activate        # Windows
# source .venv/bin/activate   # Mac/Linux

pip install -r requirements.txt
```

---

## 🔑 Configuration

Create a `.env` file in the project root:

```env
OPENAI_API_KEY=sk-your-openai-key-here
TAVILY_API_KEY=tvly-your-tavily-key-here
```

Get your API keys:
- **OpenAI / OpenRouter**: [openrouter.ai](https://openrouter.ai) or [platform.openai.com](https://platform.openai.com)
- **Tavily**: [tavily.com](https://tavily.com) — free tier available

---

## 🚀 Usage

```bash
# Activate your virtual environment
.venv\Scripts\activate

# Run the app
streamlit run app.py
```

Then open `http://localhost:8501` in your browser.

**Web Research Mode:**
1. Type a topic in the input field
2. Click **Launch Research Pipeline**
3. Watch all four agents run in sequence
4. Download the final report

**Document Mode:**
1. Upload a PDF, image, or text file
2. Type your question about the document
3. Click **Launch Research Pipeline**
4. The RAG pipeline answers using your document as the source

---

## ☁️ Deployment

### Streamlit Community Cloud (Free)

1. Push the project to a GitHub repository
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Click **New app** → select your repo → set main file to `app.py`
4. Under **Advanced settings**, add your secrets:

```toml
OPENAI_API_KEY = "Your_OPENAI_API_KEY"
TAVILY_API_KEY = "Your_TAVILY_API_KEY"
```

5. Click **Deploy** — your app gets a public URL instantly

> Make sure `packages.txt` contains `tesseract-ocr` for OCR support on the cloud.

---

## 📸 Screenshots

> The dark sci-fi editorial UI with animated pipeline status, hero section, and premium typography.

| Input Panel | Pipeline Running | Final Report |
|---|---|---|
| Topic input + file upload | Live agent status cards | Structured markdown report |

---

## 📄 License

This project is licensed under the MIT License.

---

<div align="center">
Built with using LangChain · Streamlit · OpenAI · Tavily · ChromaDB
</div>
