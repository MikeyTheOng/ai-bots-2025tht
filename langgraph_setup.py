from langgraph.prebuilt import create_react_agent
from langchain_core.messages import BaseMessage
from llm_setup import LLMSetup
from tool_setup import ToolSetup

class LangGraphSetup:
    def __init__(self, llm_setup=None, tool_setup=None):
        self.llm_setup = llm_setup if llm_setup else LLMSetup()
        self.tool_setup = tool_setup if tool_setup else ToolSetup()
        
        self.system_prompt = """You are a research assistant that helps users generate research reports.

        You MUST provide URL citations to back up your claims.
        If you are unsure, do not include it in the response.
        After each claim or piece of information, include the source URL in square brackets: [URL].

        Your final response MUST follow this structure:
        1. **Summary**: A clear, concise summary of your findings
        2. **Detailed Information**: Organized in paragraphs or bullet points with proper formatting
        3. Each claim must end with a citation to its source [URL]
        4. **References**: At the end of your response, include a "References" section with a numbered list of all URLs used

        Make sure your answers properly cite information from PubMed, Arxiv, Wikipedia, or web search results.
        """
        
        self.graph = create_react_agent(
            self.llm_setup.get_model(), 
            tools=self.tool_setup.get_tools(), 
            prompt=self.system_prompt, 
            name="research_agent"
        )

    def _extract_message_content(self, message: BaseMessage, truncate=True) -> dict:
        """
        Extracts role and content from a LangChain message object.
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
        
        self._log_message(message, truncate=truncate)
        return result

    def _log_message(self, message, truncate=True):
        """
        Logs a message in a clean, readable format based on its type.
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

    def research(self, user_input):
        """
        Process a user research query through the LangGraph agent.
        Returns the complete conversation history with properly formatted messages.
        """
        formatted_input = {"messages": [{"role": "user", "content": user_input}]}
        results = []
        
        print("\n--- Starting Research Process ---")
        
        for s in self.graph.stream(formatted_input, stream_mode="values"):
            message = s["messages"][-1]
            results.append(self._extract_message_content(message, False))
        
        print("\n--- Research Complete ---\n")
        return results if results else [{"role": "assistant", "content": "No response generated."}]