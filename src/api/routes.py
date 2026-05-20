"""
API routes for RAG operations.
"""

from fastapi import APIRouter, UploadFile, File, Header
from langchain_core.messages import HumanMessage, AIMessage, BaseMessage
from fastapi import HTTPException
import uuid

from src.memory.chathistory_mongo import ChatHistory
from src.schemas import QueryRequest
from src.rag.document_upload import documents
from src.rag.graph_builder import builder

router = APIRouter()

@router.post("/rag/query")
async def rag_query(req: QueryRequest):
    """
    Process a RAG query and return the result.

    Args:
        req: The query request containing query text and session_id.

    Returns:
        The generated response from the RAG pipeline.
    """

    #chat_history = ChatInMemoryHistory.get_session_history(req.token)
    chat_history = ChatHistory.get_session_history(req.session_id)
    await chat_history.add_message(HumanMessage(content=req.query))

    # Fetch full history
    messages = await chat_history.get_messages()
    result = builder.invoke({
        "messages": messages
    })
    last_message = result["messages"][-1]

    # Extract plain string content regardless of message type
    # graph nodes return either a BaseMessage or a dict {"role": ..., "content": ...}
    if isinstance(last_message, BaseMessage):
        output_text = last_message.content
    elif isinstance(last_message, dict):
        output_text = last_message.get("content", "")
    else:
        output_text = str(last_message)

    # Save assistant message
    await chat_history.add_message(AIMessage(content=output_text))

    return {"result":result["messages"][-1]}


@router.post("/rag/documents/upload")
async def upload_file(
    file: UploadFile = File(...),
):
    """
    Upload a document for RAG processing.

    Args:
        file: The file to upload (PDF or TXT).

    Returns:
        Upload status.
    """
    status_upload = documents(file)
    return {"status": status_upload}
    