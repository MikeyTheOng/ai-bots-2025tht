from langchain_openai import ChatOpenAI
import os
from dotenv import load_dotenv

class LLMSetup:
    def __init__(self):
        load_dotenv()
        
        open_ai_key = os.getenv("OPENAI_API_KEY")
        if open_ai_key is None:
            raise AssertionError("OPENAI_API_KEY is not set in .env file")
            
        self.model = ChatOpenAI(
            model="gpt-4o-mini", 
            temperature=0, 
            api_key=open_ai_key
        )
    
    def get_model(self):
        return self.model