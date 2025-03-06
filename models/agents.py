from beanie import Document
from pydantic import BaseModel, Field
from typing import List, Optional

class File(BaseModel):
    """
    Attributes
        name (str): File name
        text (str): Extracted text
        tokens (int): Tokens utilized by the text
    """
    name: str
    text: str
    tokens: int = Field(default=0)

class CreateAgent(BaseModel):
    """
    Attributes
        name (str): Name of the Agent
    """
    name: str

class AgentDB(Document):
    """
    Attributes
        name (str): Name of the Agent
        files (list[File]): Files to access
        messages (list[str]): All prompts by user
    """
    name: str
    files: List[File] = Field(default=[])
    messages: List[str] = Field(default=[])
    
    class Settings:
        name = "agents"