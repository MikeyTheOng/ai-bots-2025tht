from api.routes.agents import router as agents_router
from contextlib import asynccontextmanager
from db.init_db import init_mongodb
from fastapi import FastAPI
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        app.mongodb_client = await init_mongodb()
        db = app.mongodb_client.get_database("i-love-mongo")
        collections = await db.list_collection_names()
        
        logger.info(f"✅ MongoDB connection successful! Found collections: {collections}")
        
    except Exception as e:
        logger.error(f"❌ MongoDB connection failed: {str(e)}")
        raise e
    
    yield
    
    if hasattr(app, "mongodb_client"):
        app.mongodb_client.close()

app = FastAPI(lifespan=lifespan)

app.include_router(agents_router)

@app.get("/")
def read_root():
    return {"Hello": "World"}