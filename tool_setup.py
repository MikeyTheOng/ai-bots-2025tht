from langchain_core.tools import tool
import wikipedia

@tool
def get_info_from_wikipedia(topic: str) -> dict:
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

tools = [get_info_from_wikipedia]