# app/db/init_db.py
import os
from typing import Optional
from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient

from db.models.user import UserDB

async def init_mongodb(db_url: Optional[str] = None):
    """
    Initialize MongoDB connection and Beanie.
    """
    
    if db_url is None:
        db_url = os.getenv("MONGODB_URL", "mongodb://admin:password@localhost:27017/")
    
    client = AsyncIOMotorClient(db_url)
    
    await init_beanie(
        database=client["i-love-mongo"],
        document_models=[
            UserDB,
        ]
    )
    
    return client
