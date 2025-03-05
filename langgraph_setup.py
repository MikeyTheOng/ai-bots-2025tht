from langgraph.prebuilt import create_react_agent
from llm_setup import model
from tool_setup import tools
from langchain_core.messages import BaseMessage

system_prompt = """You are a research assistant that helps users find information. 
You MUST provide citations to back up your claims. 
If you are unsure, do not include it in the response.
When you use information from a tool, you MUST cite the tool as a source like this: [Source: Tool Name].
Format the final answer clearly and include all relevant information from tools.
"""

graph = create_react_agent(model, tools=tools, prompt=system_prompt, name="research_agent")
# TODO: Get name from db
# TODO: Adjust response format

def _extract_message_content(message: BaseMessage, truncate=True) -> dict:
    """
    Extracts role and content from a LangChain message object.
    
    Args:
        message: The message to extract content from
        truncate: Whether to truncate log messages (default: True)
    """
    result = {"role": message.type, "content": message.content}
    
    if message.type == "ai" and not message.content and hasattr(message, "additional_kwargs"):
        if "tool_calls" in message.additional_kwargs:
            tool_calls = message.additional_kwargs["tool_calls"]
            if tool_calls:
                result["tool_calls"] = [{
                    "name": tc["function"]["name"],
                    "arguments": tc["function"]["arguments"]
                } for tc in tool_calls]
    
    _log_message(message, truncate=truncate)
    return result

def _log_message(message, truncate=True):
    """
    Logs a message in a clean, readable format based on its type.
    
    Args:
        message: The message object to log
        truncate: Whether to truncate long content (default: True)
    """
    message_type = message.type.upper() if hasattr(message, 'type') else 'UNKNOWN'
    
    if hasattr(message, "content") and message.content:
        if truncate:
            preview = message.content[:100] + ('...' if len(message.content) > 100 else '')
        else:
            preview = message.content
        print(f"\n[{message_type}]: {preview}")
    
    elif hasattr(message, "additional_kwargs") and "tool_calls" in message.additional_kwargs:
        tool_calls = message.additional_kwargs["tool_calls"]
        for tc in tool_calls:
            name = tc["function"]["name"]
            args = tc["function"]["arguments"]
            print(f"\n[{message_type} TOOL REQUEST]: {name} with args: {args}")
    
    elif hasattr(message, "tool_calls") and message.tool_calls:
        tool_call = message.tool_calls[0]
        print(f"\n[TOOL REQUEST]: Using {tool_call['name']} with args: {tool_call['args']}")
    
    else:
        print(f"\n[{message_type}]: {str(message)[:100]}...")

def research(user_input):
    """
    Process a user research query through the LangGraph agent.
    Returns the complete conversation history with properly formatted messages.
    """
    formatted_input = {"messages": [{"role": "user", "content": user_input}]}
    results = []
    
    print("\n--- Starting Research Process ---")
    for s in graph.stream(formatted_input, stream_mode="values"):
        message = s["messages"][-1]
        results.append(_extract_message_content(message, False))
    
    print("\n--- Research Complete ---\n")
    return results if results else [{"role": "assistant", "content": "No response generated."}]