# CodeInsight-AI
An AI-powered tool that allows you to ask questions about any GitHub repository and get intelligent, context-aware answers using Retrieval-Augmented Generation (RAG).

# Features

**Repo Indexing** — fetches all code files from any public GitHub repository

**Semantic Search** — splits files into chunks, embeds them with OpenAI, stores in FAISS vector store

**Chat Interface** — ask questions in plain English, get answers grounded in the actual code

**Source References** — every answer shows which files and snippets were used

**Session Memory** — chat history persists during your session

**One-click Reset** — clear the current repo and start fresh

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

**Language**: Python

**LLM**: Groq (LLaMA 3.x)

**Framework**: LangChain

**Vector DB**: FAISS

**Embeddings**: HuggingFace (BGE / MiniLM)

**Frontend**: Streamlit

**Data Source**: GitHub REST API

**Concurrency**: ThreadPoolExecutor

# Installation
```bash
pip install -U streamlit langchain langchain-core langchain-community langchain-huggingface langchain-groq faiss-cpu python-dotenv requests4
```
# Setup

Create a .env file:
```bash
GROQ_API_KEY=your_groq_api_key
```
(Optional for higher rate limits)
```bash
GITHUB_TOKEN=your_github_token
```
# Run the App
```bash
streamlit run app.py
```
The app opens at http://localhost:8501 automatically.

# Limitations

Only works with public GitHub repositories

Very large repos (1000+ files) may be slow to index and exceed token limits

Answers are only as good as the retrieved chunks — deeply nested logic may not be captured

The vector store is in-memory and is rebuilt on every new repo analysis

# Demo - Video Walkthrough

https://drive.google.com/file/d/19yNabmZyy5BnJQzSVsZtutYKb73rM3de/view?usp=sharing
