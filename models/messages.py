from pydantic import BaseModel

class Message(BaseModel):
    """
    User message
    
    Attributes:
        message (str): User inputs
    """
    message: str