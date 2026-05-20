"""
API client for communicating with backend services.
"""

import logging
import os
import requests

logger = logging.getLogger(__name__)

# Backend service URLs
BASE_URL = "http://localhost:8000"


def query_backend(query: str, session_id: str) -> str:
    """
    Send a query to the RAG backend.

    Args:
        query: The user's query text.
        session_id: Session identifier for tracking conversation.

    Returns:
        Response text from the backend or error message.
    """
    url = f"{BASE_URL}/rag/query"
    print(f"query_backend Calling: {url}")

    response = requests.post(
        url,
        json= {"query": query, "session_id": session_id},
        allow_redirects= False
    )

    if response.status_code == 200:
        return response.json()['result']["content"]
    else:
        return f"Error: {response.status_code} - {response.text}"
    
def document_upload_rag(file) -> bool:
    """
    Upload a document to the RAG system.

    Args:
        file: File object to upload.

    Returns:
        True if upload succeeds, False otherwise.
    """
    url = f"{BASE_URL}/rag/documents/upload"

    if file:
        files = {"file": (file.name, file, file.type)}
        response = requests.post(url, files=files)
        print(response)

        if response.status_code == 200:
            return True
    
    return False
