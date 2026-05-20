"""
MongoDB client initialization
"""

import os
import certifi
from pathlib import Path
from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient

# Force load .env from project root
load_dotenv(dotenv_path=Path(__file__).resolve().parents[2] / ".env")

MONGO_URL = os.getenv("MONGO_URI")
DB_NAME = os.getenv("MONGO_DB_NAME", "adaptive_rag")

if not MONGO_URL:
    raise ValueError("MONGO_URI is not set in .env file")

print(f"Connecting to MongoDB: {MONGO_URL[:40]}...")

client = AsyncIOMotorClient(
    MONGO_URL,
    tls=True,
    tlsCAFile=certifi.where()
)

db = client[DB_NAME]