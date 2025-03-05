from duckduckgo_search import DDGS
from langchain_core.tools import tool
import wikipedia

@tool
def search_wikipedia(topic: str) -> dict:
    """
    Get information about a topic from Wikipedia.
    """
    try:
        page = wikipedia.page(topic)
        summary = wikipedia.summary(topic, sentences=5)
        return {
            "title": page.title,
            "url": page.url,
            "summary": summary,
            "status": "success"
        }
    except wikipedia.exceptions.DisambiguationError as e:
        options = e.options[:5]
        options_with_summaries = []
        for option in options:
            try:
                summary = wikipedia.summary(option, sentences=5)
                options_with_summaries.append({
                    "title": option,
                    "summary": summary
                })
            except (wikipedia.exceptions.DisambiguationError, wikipedia.exceptions.PageError, Exception):
                options_with_summaries.append({
                    "title": option,
                    "summary": "No summary available"
                })
                
        return {
            "status": "disambiguation_error",
            "query": topic,
            "options": options_with_summaries,
            "message": f"'{topic}' may refer to multiple topics. Please be more specific."
        }
    except wikipedia.exceptions.PageError:
        return {
            "status": "page_error",
            "query": topic,
            "message": f"No Wikipedia article found for '{topic}'. Try another search term."
        }
    except Exception as e:
        return {
            "status": "error",
            "query": topic,
            "message": f"Error retrieving information: {str(e)}"
        }
        
@tool
def search_web_with_duckduckgo(query: str, max_results: int = 5) -> dict:
    """
    Perform a general web search using DuckDuckGo.
    """
    try:
        ddgs = DDGS()
        results = ddgs.text(
            keywords=query,
            region="wt-wt",
            safesearch="moderate",
            max_results=max_results
        )
        
        formatted_results = []
        for result in results:
            formatted_results.append({
                "title": result.get("title", "No title"),
                "body": result.get("body", "No body text"),
                "href": result.get("href", "No URL")
            })
        
        return {
            "status": "success",
            "query": query,
            "results": formatted_results
        }
    
    except Exception as e:
        return {
            "status": "error",
            "query": query,
            "message": f"Error performing search: {str(e)}"
        }

@tool
def search_duckduckgo_news(query: str, max_results: int = 5, time_period: str = None) -> dict:
    """
    Search for news articles using DuckDuckGo News.
    """
    try:
        ddgs = DDGS()
        results = ddgs.news(
            keywords=query,
            region="wt-wt",
            safesearch="moderate",
            timelimit=time_period,
            max_results=max_results
        )
        
        formatted_results = []
        for result in results:
            formatted_results.append({
                "title": result.get("title", "No title"),
                "body": result.get("body", "No body text"),
                "url": result.get("url", "No URL"),
                "date": result.get("date", "No date"),
                "source": result.get("source", "Unknown source"),
                "image": result.get("image", None)
            })
        
        return {
            "status": "success",
            "query": query,
            "time_period": time_period if time_period else "all time",
            "results": formatted_results
        }
    
    except Exception as e:
        return {
            "status": "error",
            "query": query,
            "message": f"Error performing news search: {str(e)}"
        }

tools = [search_wikipedia, search_web_with_duckduckgo, search_duckduckgo_news]
class ToolSetup:
    def __init__(self):
        self.tools = tools
    
    def get_tools(self):
        return self.tools