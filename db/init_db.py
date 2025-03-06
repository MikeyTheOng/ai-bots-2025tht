import logging
import os
from beanie import init_beanie
from models.agents import AgentDB
from motor.motor_asyncio import AsyncIOMotorClient
from typing import Optional

logger = logging.getLogger(__name__)

async def init_mongodb(db_url: Optional[str] = None):
    """
    Initialize MongoDB connection and Beanie.
    """
    try:
    
        if db_url is None:
            db_url = os.getenv("MONGODB_URL", "mongodb://admin:password@localhost:27017/")
        
        client = AsyncIOMotorClient(db_url)
        
        await init_beanie(
            database=client["i-love-mongo"],
            document_models=[
                AgentDB,
            ]
        )
        
        return client
    except Exception as e:
        logger.error(f"Failed to connect to MongoDB: {str(e)}")
        raise
