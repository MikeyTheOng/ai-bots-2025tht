from beanie import Document
from pydantic import BaseModel

class CreateAgent(BaseModel):
    """Schema for creating a new Agent"""
    name: str

class AgentDB(Document):
    """Agent document stored in MongoDB"""
    name: str
    
    class Settings:
        name = "agents"