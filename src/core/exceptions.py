"""
Custom HTTP exceptions so the API always returns structured JSON errors instead of raw 500s.
"""

from fastapi import HTTPException

class RagQueryError(HTTPException):
    def __init__(self, detail: str):
        super().__init__(status_code=500, detail=detail)

class DocumentIngestionError(HTTPException):
    def __init__(self, detail: str):
        super().__init__(status_code=422, detail=detail)