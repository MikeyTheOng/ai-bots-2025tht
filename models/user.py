from beanie import Document
from pydantic import BaseModel

class UserCreate(BaseModel):
    """Schema for creating a new User"""
    name: str


class UserDB(Document):
    """User document stored in MongoDB"""
    name: str
    
    class Settings:
        name = "users"
