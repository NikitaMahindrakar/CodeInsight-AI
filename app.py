# import streamlit as st
# from dotenv import load_dotenv

# from repo_loader import clone_repo, load_code_files
# from rag_engine import build_vector_store, create_qa_chain

# load_dotenv()

# st.title("AI Codebase Explainer")

# repo_url = st.text_input("Enter GitHub Repository URL")

# if st.button("Analyze Repo"):

#     repo_path = clone_repo(repo_url)
#     files = load_code_files(repo_path)
#     vectorstore = build_vector_store(files)
#     qa_chain = create_qa_chain(vectorstore)
#     st.session_state.qa = qa_chain
#     st.success("Repository indexed successfully!")

# question = st.text_input("Ask a question about the codebase")

# if question and "qa" in st.session_state:

#     result = st.session_state.qa.invoke({"query": question})
#     st.write(result["result"])

import streamlit as st
from dotenv import load_dotenv

from rag.loader import fetch_repo_files
from rag.splitter import split_documents
from rag.embeddings import get_embeddings
from rag.vectorstore import build_vectorstore
from rag.qa_chain import create_qa_chain

load_dotenv()

st.set_page_config(page_title="CodeInsight AI", layout="wide")
st.title("🚀 CodeInsight AI")

# --------------------------
# SESSION STATE
# --------------------------
if "current_repo" not in st.session_state:
    st.session_state.current_repo = None

if "qa" not in st.session_state:
    st.session_state.qa = None

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "repo_stats" not in st.session_state:
    st.session_state.repo_stats = None

# --------------------------
# CACHE
# --------------------------
@st.cache_resource
def setup_pipeline(repo_url):
    docs = fetch_repo_files(repo_url)
    chunks = split_documents(docs)
    embeddings = get_embeddings()
    vectorstore = build_vectorstore(chunks, embeddings)
    qa_chain = create_qa_chain(vectorstore)
    return qa_chain, len(docs), len(chunks)

# --------------------------
# SIDEBAR (Controls)
# --------------------------
with st.sidebar:
    st.header("⚙️ Controls")

    repo_url = st.text_input("GitHub Repo URL")

    if st.button("🔍 Analyze Repo"):
        if repo_url:
            st.cache_resource.clear()

            with st.spinner("Fetching & indexing repo..."):
                try:
                    qa_chain, file_count, chunk_count = setup_pipeline(repo_url)

                    st.session_state.qa = qa_chain
                    st.session_state.current_repo = repo_url
                    st.session_state.repo_stats = (file_count, chunk_count)
                    st.session_state.chat_history = []

                    st.success("✅ Repo indexed!")
                except Exception as e:
                    st.error(f"Error: {str(e)}")

    if st.button("🧹 Reset"):
        st.session_state.clear()
        st.rerun()

# --------------------------
# MAIN UI
# --------------------------

# Show repo info
if st.session_state.current_repo:
    st.info(f"📦 Current Repo: {st.session_state.current_repo}")

    if st.session_state.repo_stats:
        file_count, chunk_count = st.session_state.repo_stats
        col1, col2 = st.columns(2)
        col1.metric("Files", file_count)
        col2.metric("Chunks", chunk_count)

# --------------------------
# CHAT UI
# --------------------------
st.subheader("💬 Ask Questions")

# Display chat history
for chat in st.session_state.chat_history:
    with st.chat_message("user"):
        st.write(chat["question"])
    with st.chat_message("assistant"):
        st.write(chat["answer"])

# Input box (chat style)
question = st.chat_input("Ask about the codebase...")

if question and st.session_state.qa:
    with st.chat_message("user"):
        st.write(question)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            result = st.session_state.qa.invoke({"query": question})
            answer = result["result"]

            st.write(answer)

            # Save chat
            st.session_state.chat_history.append({
                "question": question,
                "answer": answer
            })

            # Sources
            with st.expander("📂 Sources"):
                for doc in result["source_documents"]:
                    st.write(f"📄 {doc.metadata.get('source')}")
                    st.code(doc.page_content[:300])