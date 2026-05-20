"""
Retriever setup and vector store configuration
"""

import os
from dotenv import load_dotenv
from src.core.config import Settings

from langchain_core.documents import Document
from langchain_core.tools import create_retriever_tool
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_qdrant import QdrantVectorStore
from langchain_community.vectorstores import FAISS

load_dotenv()
HF_TOKEN = os.getenv("HF_TOKEN")
embeddings = HuggingFaceEmbeddings(model_name="BAAI/bge-m3")



def retriever_chain(chunks: list[Document]):
    """
    Initialize and store documents in vector database

    Args:
        chunks: List of document chunks to store.

    Returns:
        Boolean indicating success of the operation
    """
    try:
        vectorstore = QdrantVectorStore.from_documents(
            documents=chunks,
            embedding=embeddings,
            url=Settings.QDRANT_URL,
            api_key = Settings.QDRANT_API_KEY,
            collection_name = Settings.CODE_COLLECTION
        )

        retriever = vectorstore.as_retriever()

        print("Qdrant vector store initialted with documents")
        print(f"vectorstore contains {len(chunks)} documeny chunks")
        return True
    except Exception as e:
        print(f"error storing documnets in Qdrant: {e}")
        return False
    
def get_retriever():
    """
    Get a retriever tool connected to the vector store.

    Returns the retriever tool that can search documents stored by retriever_chain().
    If no documents have been uploaded yet, creates a retriever with a dummy document.

    Returns:
        A LangChain retriever tool configured for the vector store.

    Raises:
        Exception: If vector store initialization fails.   
    """
    try:
        vectorstore = QdrantVectorStore.from_existing_collection(
                embedding=embeddings,
                url=Settings.QDRANT_URL,
                api_key=Settings.QDRANT_API_KEY,
                collection_name=Settings.CODE_COLLECTION,
            )
        retriever = vectorstore.as_retriever()

        retriever_tool = create_retriever_tool(
            retriever,
            "retriever_uploaded_documents",
            f"Use this tool **only** to answer questions about the uploaded documents"
            "Don't use this tool to answer anything else."
        )
        return retriever_tool
    
    except Exception as e:
        print(f"Error initializing retriever {e}")
        raise Exception(e)


