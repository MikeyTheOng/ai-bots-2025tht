from duckduckgo_search import DDGS
from langchain_core.tools import tool
import wikipedia

class ToolSetup:
    def __init__(self):
        self.tools = [
            self.search_wikipedia,
            self.search_web_with_duckduckgo,
            self.search_duckduckgo_news
        ]
    
    def get_tools(self):
        return self.tools
    
    @tool
    def search_wikipedia(self, topic: str) -> dict:
        """
        Get information about a topic from Wikipedia.
        
        Args:
            topic: The topic to search for on Wikipedia
            
        Returns:
            A dictionary containing the page title, URL, and summary, or error information
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
    def search_web_with_duckduckgo(self, query: str, max_results: int = 5) -> dict:
        """
        Perform a general web search using DuckDuckGo to find webpages, documents, and information.
        Use this for finding general information, documentation, and websites about a topic.
        
        Args:
            query: The search query for finding general web content
            max_results: Maximum number of results to return (default: 5)
            
        Returns:
            A dictionary containing general web search results or error information
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
    def search_duckduckgo_news(self, query: str, max_results: int = 5, time_period: str = None) -> dict:
        """
        Search for news articles using DuckDuckGo News.
        
        Args:
            query: The search query for news articles
            max_results: Maximum number of results to return (default: 5)
            time_period: Time period for news search (d = day, w = week, m = month, None = all time)
            
        Returns:
            A dictionary containing news search results or error information
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