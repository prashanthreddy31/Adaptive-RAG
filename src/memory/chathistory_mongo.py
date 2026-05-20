"""
Chat history storage using MongoDB backend
"""

from datetime import datetime
from typing import List

from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.messages import BaseMessage

from src.db.mongo_client import db

collection = db["chat_history"]

class MongoDBChatHistory(BaseChatMessageHistory):
    """Chat history backed by MongoDB."""

    def __init__(self, session_id: str):
        """
        Initialize chat history for a session.

        Args:
            session_id: Unique session identifier.
        """
        self.session_id = session_id

    async def add_message(self, message: BaseMessage) -> List[BaseMessage]:
        """
        Save a message to MongoDB

        Args:
            message: The message to save
        """
        await collection.insert_one({
            "session_id": self.session_id,
            "type": message.type,
            "content": message.content,
            "additional_kwargs": message.additional_kwargs,
            "timestamp":datetime.utcnow(),
        })

    async def get_messages(self) -> List[BaseMessage]:
        """
        Load all the messages for a session from MongoDB

        returns:
             List of messages in chronological order.
        """
        from langchain_core.messages import messages_from_dict

        cursor = collection.find({"session_id":self.session_id}).sort("timestamp", 1)
        docs = await cursor.to_list(length=1000)

        # convert to BaseMessage objects
        return messages_from_dict([
            {
                "type": d["type"],
                "data": {
                    "content": d["content"],
                    "additional_kwargs": d.get("additional_kwargs", {}),
                }
            }
            for d in docs
        ])
    
    async def clear(self) -> None:
        """ Delete all messages from a session."""
        await collection.delete_many({"session_id":self.session_id})

class ChatHistory:
    """ factory for MongoDB-backed chat hidstory."""

    @classmethod
    def get_session_history(
        cls,
        session_id: str,
        config: dict = None
    ) -> MongoDBChatHistory:
        """
        Get or create chat history for a session

        Args:
            session_id: Unique session identifier.
            config: optional configuration dictionary.

        Returns:
            MongoDBChatMessageHistory instance for the session
        """
        return MongoDBChatHistory(session_id)



        