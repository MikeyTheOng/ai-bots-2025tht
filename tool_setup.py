
from langchain_core.tools import tool
from typing import Literal
@tool
def get_wiki_info(topic: str) -> str:
    """Use this to get information from Wikipedia"""
    print("Topic:", topic)
    if topic.lower() == "gundam":
        return "Gundam is a mecha anime series about doraemon flying on a boat"
    else:
        return "No info found"

tools = [get_wiki_info]