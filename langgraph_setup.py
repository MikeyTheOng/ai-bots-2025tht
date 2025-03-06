from langgraph.prebuilt import create_react_agent
from langchain_core.messages import BaseMessage
from llm_setup import LLMSetup
from tool_setup import ToolSetup
import os

class LangGraphSetup:
    def __init__(self, llm_setup=None, tool_setup=None, agent_files=None):
        self.llm_setup = llm_setup if llm_setup else LLMSetup()
        self.tool_setup = tool_setup if tool_setup else ToolSetup()
        
        script_dir = os.path.dirname(os.path.abspath(__file__))
        system_prompt_path = os.path.join(script_dir, 'system_prompt.txt')
        
        with open(system_prompt_path, 'r') as file:
            self.base_system_prompt = file.read()
        
        self._create_agent(agent_files)
        
    def _create_agent(self, agent_files=None):
        """
        Create or recreate the agent with optional file context from AgentDB
        """
        system_prompt = self._add_long_context_to_base_system_prompt(agent_files)

        self.graph = create_react_agent(
            self.llm_setup.get_model(), 
            tools=self.tool_setup.get_tools(), 
            prompt=system_prompt, 
            name="research_agent"
        )
        
    def _add_long_context_to_base_system_prompt(self, agent_files):
        system_prompt = self.base_system_prompt
        long_context = """
        ## KNOWLEDGE BASE
        Use the following information as your primary source when answering questions about specific topics. This knowledge base contains authoritative information that should take precedence over other sources.

        When referencing information from this knowledge base:
        1. Cite the specific document name in your response using the format [Agent File: Filename]
        2. Prioritize this information over general knowledge when it directly addresses the query
        3. Still follow the citation and evidence-based guidelines from your primary instructions
        """
        
        if agent_files:
            long_context+="## Agent Files Knowledge Base\n\nWhen you use any agent file, you MUST specify the file name instead of the url\n\n"
            for file in agent_files:
                long_context += f"### {file.name}\n{file.text}\n\n"
            
        system_prompt += long_context
        return system_prompt

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