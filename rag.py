
from langchain_text_splitters import RecursiveCharacterTextSplitter

from langchain_community.vectorstores import Chroma

from langchain_openai import OpenAIEmbeddings
import streamlit as st

import os

from dotenv import load_dotenv

load_dotenv()


# ── Embedding Model ─────────────────────────────

embeddings = OpenAIEmbeddings(
    api_key=st.secrets["OPENAI_API_KEY"],
    base_url="https://openrouter.ai/api/v1",
    model="text-embedding-3-small"
)


# ── Create Vector Store ─────────────────────────

def create_vector_store(document_text: str):
    if not document_text.strip():
        raise ValueError("Document content is empty.")

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )

    chunks = splitter.split_text(document_text)

    vectorstore = Chroma.from_texts( texts=chunks, embedding=embeddings )

    return vectorstore


# ── Retrieve Relevant Chunks ────────────────────

def retrieve_relevant_context(vectorstore, query: str, k: int = 4):

    docs = vectorstore.similarity_search(query, k=k)

    context = "\n\n".join([doc.page_content for doc in docs])

    return context

