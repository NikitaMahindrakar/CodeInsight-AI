# CodeInsight-AI
An AI-powered tool that allows you to ask questions about any GitHub repository and get intelligent, context-aware answers using Retrieval-Augmented Generation (RAG).

# Features
💬 Chat with any GitHub repository in natural language
⚡ Fast parallel GitHub API ingestion (no cloning required)
🧠 Context-aware answers using RAG (LangChain + FAISS + LLM)
📂 Source attribution (see exact code snippets used)
🚀 Interactive Streamlit UI (ChatGPT-like experience)
🧩 Modular, scalable, production-ready architecture

# Architecture
```bash
GitHub Repo URL
      │
      ▼
 rag/loader.py        ← fetches all code files via GitPython
      │
      ▼
 rag/splitter.py      ← splits files into overlapping chunks (LangChain)
      │
      ▼
 rag/embeddings.py    ← generates OpenAI embeddings for each chunk
      │
      ▼
 rag/vectorstore.py   ← stores embeddings in FAISS (in-memory)
      │
      ▼
 rag/qa_chain.py      ← LangChain RetrievalQA chain with GPT
      │
      ▼
 app.py               ← Streamlit UI (sidebar + chat interface)
```
 
# Tech Stack
Language: Python
LLM: Groq (LLaMA 3.x)
Framework: LangChain
Vector DB: FAISS
Embeddings: HuggingFace (BGE / MiniLM)
Frontend: Streamlit
Data Source: GitHub REST API
Concurrency: ThreadPoolExecutor

# Installation

pip install -U streamlit langchain langchain-core langchain-community langchain-huggingface langchain-groq faiss-cpu python-dotenv requests4

# Setup

Create a .env file:

GROQ_API_KEY=your_groq_api_key

(Optional for higher rate limits)

GITHUB_TOKEN=your_github_token

# Run the App
streamlit run app.py

# Demo - Video Walkthrough

https://drive.google.com/file/d/19yNabmZyy5BnJQzSVsZtutYKb73rM3de/view?usp=sharing
