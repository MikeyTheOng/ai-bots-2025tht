from langchain_openai import ChatOpenAI
import os
from dotenv import load_dotenv

load_dotenv()

open_ai_key = os.getenv("OPENAI_API_KEY")
if open_ai_key is None:
    raise AssertionError("OPENAI_API_KEY is not set in .env file")
model = ChatOpenAI(model="gpt-4o-mini", temperature=0, api_key=open_ai_key)