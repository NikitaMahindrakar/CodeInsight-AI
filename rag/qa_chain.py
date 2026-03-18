from langchain_classic.chains import RetrievalQA
from langchain_core.prompts import PromptTemplate
from langchain_groq import ChatGroq
from .config import LLM_MODEL, TOP_K


def create_qa_chain(vectorstore):
    retriever = vectorstore.as_retriever(
        search_type="mmr",
        search_kwargs={"k": TOP_K}
    )

    prompt = PromptTemplate(
        input_variables=["context", "question"],
        template="""
You are an expert software engineer analyzing a codebase.

Answer ONLY from the given context.
If not found, say: Not found in codebase.

Give clear explanation with file names.

Context:
{context}

Question:
{question}

Answer:
"""
    )

    llm = ChatGroq(
        model=LLM_MODEL,
        temperature=0,
        max_tokens=1024
    )

    return RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        return_source_documents=True,
        chain_type_kwargs={"prompt": prompt}
    )

