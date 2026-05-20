<div align="center">

# ⬡ Adaptive RAG

### *Your documents. Your questions. Answered intelligently.*

[![Python 3.10+](https://img.shields.io/badge/Python-3.10+-3776ab?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-Backend-009688?style=flat-square&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![LangGraph](https://img.shields.io/badge/LangGraph-Orchestration-ff6b35?style=flat-square)](https://python.langchain.com/langgraph/)
[![Qdrant](https://img.shields.io/badge/Qdrant-Vector-DB-6c4cdf?style=flat-square)](https://qdrant.tech/)
[![MongoDB](https://img.shields.io/badge/MongoDB-Chat-History-47a248?style=flat-square&logo=mongodb&logoColor=white)](https://mongodb.com/)
[![Groq](https://img.shields.io/badge/Groq-LLM-f55036?style=flat-square)](https://groq.com/)
[![Streamlit](https://img.shields.io/badge/Streamlit-UI-ff4b4b?style=flat-square&logo=streamlit&logoColor=white)](https://streamlit.io/)

<br/>

> Upload a PDF. Ask anything. Get precise, context-aware answers — powered by an agentic AI pipeline that thinks before it retrieves.

</div>

---

## What is Adaptive RAG?

Most RAG systems blindly retrieve documents and hope for the best. **Adaptive RAG is different.**

Before answering your question, the system classifies it — does it need your uploaded documents, general world knowledge, or a live web search? It routes accordingly, grades the retrieved content for relevance, rewrites the query if results are poor, and only then generates a response. Every query takes the path it deserves.

Built on **LangGraph** for stateful workflow orchestration, **Qdrant** for vector search, **Groq** for fast inference, and **MongoDB** for persistent conversation memory.

---

## How it works

```
Your question
      │
      ▼
┌─────────────────────┐
│   Query Classifier  │  ← LLM decides: index / general / web search
└──────────┬──────────┘
           │
     ┌─────┴──────┐──────────────┐
     ▼            ▼              ▼
┌─────────┐  ┌─────────┐  ┌───────────┐
│Retriever│  │ General │  │Web Search │
│(Qdrant) │  │   LLM   │  │ (Tavily)  │
└────┬────┘  └────┬────┘  └─────┬─────┘
     │            │             │
     ▼            │             │
┌─────────┐       │             │
│  Grader │       │             │
│relevant?│       │             │
└────┬────┘       │             │
     │            │             │
   yes│  no→ ┌────────┐         │
     │       │Rewrite │─────────┘
     │       │ Query  │
     │       └────────┘
     ▼            ▼             ▼
┌──────────────────────────────────┐
│          Generate Answer         │
└──────────────────────────────────┘
      │
      ▼
  Response  +  saved to MongoDB
```

---

## Features at a glance

**Intelligent Routing** — Three processing paths selected automatically per query: document retrieval, general knowledge, or real-time web search.

**Relevance Grading** — Retrieved chunks are scored for relevance before being used. Low-quality results trigger automatic query rewriting and a second retrieval attempt.

**ReAct Agent** — A reasoning-and-acting agent handles document retrieval, giving the system the ability to plan multi-step lookups.

**Persistent Memory** — Full conversation history stored in MongoDB Atlas, keyed by session ID. Every user gets their own context window, preserved across requests.

**Clean UI** — Streamlit interface with document upload sidebar, live chat, and an indexed documents tracker.

**Async API** — FastAPI backend with fully async MongoDB operations via Motor.

---

## Tech stack

| Layer | Technology |
|---|---|
| LLM | Groq (`llama-3.3-70b-versatile`) |
| Orchestration | LangGraph |
| Framework | LangChain |
| Vector DB | Qdrant Cloud |
| Chat Memory | MongoDB Atlas + Motor |
| Embeddings | HuggingFace (`BAAI/bge-m3`) |
| Web Search | Tavily |
| Backend | FastAPI + Uvicorn |
| Frontend | Streamlit |
| Validation | Pydantic v2 |

---

## Project structure

```
Adaptive-RAG/
├── src/
│   ├── main.py                     # FastAPI app entry point
│   ├── api/
│   │   └── routes.py               # /rag/query and /rag/documents/upload
│   ├── core/
│   │   ├── config.py               # Core configuration
│   │   └── settings.py             # Prompt loading and app settings
│   ├── db/
│   │   └── mongo_client.py         # MongoDB Atlas connection
│   ├── llms/
│   │   └── groq.py                 # Groq LLM initialization
│   ├── memory/
│   │   ├── chathistory_mongo.py    # MongoDB-backed chat history
│   │   └── chatHistory_in_memory.py
│   ├── rag/
│   │   ├── graph_builder.py        # LangGraph workflow
│   │   ├── retriever_setup.py      # Qdrant vector store + retriever tool
│   │   ├── document_upload.py      # Document ingestion pipeline
│   │   └── ReAct_agent.py          # ReAct agent setup
│   ├── schemas/
│   │   └── __init__.py             # Pydantic models (State, Grade, Route...)
│   └── tools/
│       └── graph_tools.py          # Routing and grading conditional edges
│
├── streamlit_app/
│   ├── home.py                     # Main chat UI
│   └── utils/
│       └── api_client.py           # HTTP client for FastAPI backend
│
├── .env                            # Environment variables (never commit)
├── requirements.txt
└── README.md
```

---

## Quick start

### 1. Clone and install

```bash
git clone https://github.com/your-username/Adaptive-RAG.git
cd Adaptive-RAG
python -m venv .venv
.venv\Scripts\activate        # Windows
# source .venv/bin/activate   # macOS/Linux
pip install -r requirements.txt
```

### 2. Set up environment variables

Create a `.env` file in the project root:

```env
# Groq
GROQ_API_KEY=your_groq_api_key

# Qdrant
QDRANT_URL=https://your-cluster.qdrant.io
QDRANT_API_KEY=your_qdrant_api_key
CODE_COLLECTION=your_collection_name

# MongoDB Atlas
MONGO_URI= your_MongoDB_URI
MONGO_DB_NAME= your_Db_name

# HuggingFace
HF_TOKEN=hf_your_token

# Tavily (web search)
TAVILY_API_KEY=your_tavily_api_key
```

### 3. Start the backend

```bash
uvicorn src.main:app --reload
```

API will be live at `http://localhost:8000`.
Interactive docs at `http://localhost:8000/docs`.

### 4. Start the frontend

```bash
streamlit run streamlit_app/home.py
```

---

## API reference

### `POST /rag/query`

Send a question and get an AI-generated response.

```http
POST /rag/query
Content-Type: application/json

{
  "query": "What is the attention mechanism?",
  "session_id": "550e8400-e29b-41d4-a716-446655440000"
}
```

```json
{
  "result": {
    "content": "The attention mechanism allows a model to focus on..."
  }
}
```

---

### `POST /rag/documents/upload`

Upload a PDF or TXT file for indexing.

```http
POST /rag/documents/upload
Content-Type: multipart/form-data

file: <your-document.pdf>
```

```json
{
  "status": true
}
```

Supported formats: `.pdf`, `.txt`

---

## Graph nodes explained

| Node | What it does |
|---|---|
| `query_analysis` | Classifies query → index / general / search |
| `retriever` | Runs ReAct agent to fetch relevant chunks from Qdrant |
| `grade` | Scores retrieved chunks for relevance (yes/no) |
| `rewrite` | Rewrites query if grading fails, loops back to retriever |
| `generate` | Produces final answer from retrieved context |
| `web_search` | Fetches live results via Tavily when query needs it |
| `general_llm` | Answers directly from LLM when no docs are needed |

---

## Environment variable reference

| Variable | Description |
|---|---|
| `GROQ_API_KEY` | Groq API key for LLM inference |
| `QDRANT_URL` | Qdrant Cloud cluster URL |
| `QDRANT_API_KEY` | Qdrant authentication key |
| `CODE_COLLECTION` | Qdrant collection name for document storage |
| `MONGO_URI` | MongoDB Atlas connection string |
| `MONGO_DB_NAME` | MongoDB database name |
| `HF_TOKEN` | HuggingFace token for embedding model download |
| `TAVILY_API_KEY` | Tavily API key for web search |

---

## FAQ

**The upload returns 500.**
Check that your Qdrant cluster is active and `CODE_COLLECTION` matches an existing collection or that `from_documents` can create it. Also verify `pypdf` is installed.

**MongoDB SSL handshake error on Windows.**
Install `certifi` and pass `tlsCAFile=certifi.where()` to `AsyncIOMotorClient`. This is a Windows OpenSSL issue, not a credentials issue.

**Groq structured output fails.**
Use `llama-3.3-70b-versatile` — it has the best tool-calling support on Groq. Avoid lesser-known or preview model names.

**Query returns 500 after MongoDB connects.**
Check `routes.py` — the last message from the graph may be a dict `{"role": "assistant", "content": "..."}`. Extract `.get("content")` before passing to `AIMessage`.

**How is conversation memory maintained?**
Each browser session generates a UUID stored in `st.session_state`. This is passed as `session_id` with every query. MongoDB stores all messages under that ID in chronological order.

---

## Roadmap

- [ ] Multi-document collections with separate namespaces
- [ ] Streaming responses to the frontend
- [ ] Analytics dashboard (query types, latency, routing stats)
- [ ] Multi-language document support
- [ ] Docker + docker-compose setup
- [ ] Extended LLM provider support (OpenAI, Anthropic)
- [ ] Rate limiting and usage quotas

---

## Contributing

Pull requests are welcome.

```bash
git checkout -b feature/your-feature
# make changes
git commit -m "feat: describe your change"
git push origin feature/your-feature
```

Please follow PEP 8, add docstrings to all functions, and test before opening a PR.


<div align="center">

Built with LangGraph · Qdrant · Groq · MongoDB · Streamlit

</div>
