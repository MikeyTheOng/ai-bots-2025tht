from langchain_core.tools import tool
import wikipedia

@tool
def get_info_from_wikipedia(topic: str) -> str:
    """
    Get information about a topic from Wikipedia.
    
    Args:
        topic: The topic to search for on Wikipedia
        
    Returns:
        A summary of the Wikipedia article or an error message
    """
    try:
        summary = wikipedia.summary(topic, sentences=5)
        return summary
    except wikipedia.exceptions.DisambiguationError as e:
        options = e.options[:5]
        return f"'{topic}' may refer to multiple topics: {', '.join(options)}. Please be more specific."
    except wikipedia.exceptions.PageError:
        return f"No Wikipedia article found for '{topic}'. Try another search term."
    except Exception as e:
        return f"Error retrieving information: {str(e)}"

tools = [get_info_from_wikipedia]