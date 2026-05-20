"""
Document upload and processing module.
"""

import os
import tempfile

from fastapi import UploadFile, File
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

from src.rag.retriever_setup import retriever_chain

def documents(file: UploadFile = File(...)):
    """
    Process and upload a document for RAG.

    Validates file type, load content, chunks documents,
    and stores them in the vector database.

    Args:
        file: The uploaded file (PDF or TXT).

    Returns:
    Boolean indicating success of the ipload process.
    """
    filename = file.filename
    print(filename)
    if not filename.endswith(".pdf") and not filename.endswith(".txt"):
        from fastapi import HTTPException
        raise HTTPException(
            status_code=400,
            detail="Only PDF and TXT files are supported"
        )
    
    file_bytes = file.file.read()

    with tempfile.NamedTemporaryFile(
        delete=False,
        suffix=os.path.splitext(filename)[1]
    ) as tmp_file:
        tmp_file.write(file_bytes)
        tmp_path = tmp_file.name

    if filename.endswith(".pdf"):
        loader = PyPDFLoader(tmp_path)
    else:
        loader = TextLoader(tmp_path)

    try:
        docs = loader.load()
    except Exception as e:
        from fastapi import HTTPException
        raise HTTPException(
            status_code=500,
            detail=f"Error loading file: {e}"
        )
    finally:
        os.unlink(tmp_path)

    # Split the documents into chunks
    Splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap = 200
    )

    chunks = Splitter.split_documents(docs)

    return retriever_chain(chunks)