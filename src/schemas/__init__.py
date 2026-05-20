from pydantic import BaseModel, Field
from typing import TypedDict, Annotated, Optional

from langchain_core.messages import AnyMessage
from langgraph.graph import add_messages

class Grade(BaseModel):
    """Model for grading relevance of retrieved documents."""

    binary_score:str = Field(
        description="Relevance score : 'yes' or 'no'"
    )

class QueryRequest(BaseModel):
    """ Request model for RAG queries."""

    query: str
    session_id: str

class RouteIdentifier(BaseModel):
    """Model for routing queries to appropriate nodes."""

    route: str

class State(TypedDict):
    """State schema for the RAG graph"""

    messages: str = Annotated[list[AnyMessage], add_messages]
    binary_score: Optional[str]
    route: Optional[str]
    latest_query: Optional[str]

class VerificationResult(BaseModel):
    """ Model for verifying answer faithfulness."""

    faithful: bool = Field(
        description="True if answer is supported by the context."
    )
    explaination: str = Field(
        description="Brief reasoning"
    )
