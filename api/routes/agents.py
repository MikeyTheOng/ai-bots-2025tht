from fastapi import APIRouter, Form, HTTPException
import json
from db.agents import create_agent, delete_agent, get_agent, update_agent_messages
from langgraph_setup import LangGraphSetup
from llm_setup import LLMSetup
from models.agents import AgentDB, CreateAgent
from models.messages import Message
from tool_setup import ToolSetup
from typing import Dict

router = APIRouter()

llm_setup = LLMSetup()
tool_setup = ToolSetup()
langgraph_setup = LangGraphSetup(llm_setup, tool_setup)

@router.post("/agents", status_code=201, response_model=Dict[str, str])
async def create_agent_route(
    agent_post: str = Form(...),
):
    """
    Create a new research agent
    
    Args:
        agent: JSON string containing agent details
    
    Returns:
        Newly created agent ID
    """
    try:
        agent_data = json.loads(agent_post)
        validated_agent = CreateAgent(**agent_data)
        new_agent = await create_agent(validated_agent)
        return {"agent_id": str(new_agent.id)}
    except json.JSONDecodeError:
        raise HTTPException(status_code=422, detail="Invalid JSON in agent_post")
    except ValueError as e:
        raise HTTPException(status_code=422, detail=f"Invalid agent data: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating agent: {str(e)}")
    
@router.get("/agents/{agent_id}", status_code=200, response_model=AgentDB)
async def get_agent_route(
    agent_id: str,
):
    """
    Get a research agent by ID

    Args:
        agent_id: ID of the agent to retrieve

    Returns:
        Agent details
    """
    try:
        agent = await get_agent(agent_id)
        if not agent:
            return AgentDB(name="")
        return agent
    except ValueError as e:
        raise HTTPException(status_code=422, detail=f"Validation error: {str(e)}")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving agent: {str(e)}")

@router.delete("/agents/{agent_id}", status_code=204)
async def delete_agent_route(
    agent_id: str,
):
    """
    Delete a research agent by ID
    Args:
        agent_id: ID of the agent to delete
    Returns:
        None
    """
    try:
        await delete_agent(agent_id)
    except ValueError as e:
        raise HTTPException(status_code=422, detail=f"Validation error: {str(e)}")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving agent: {str(e)}")
    
@router.post("/agents/{agent_id}/queries", status_code=201)
async def send_message_route(
    agent_id: str,
    message: Message
):
    """
    Sends a user prompt to the Research Agent and returns the research conducted
    
    Args:
        agent_id: ID of the agent to send the message to
        message: Message containing the user prompt
        
    Returns:
        Research results
    """
    try:
        query = message.message
        agent = await get_agent(agent_id)
        if not agent:
            return {"role": "system", "content": "Agent not found."}
        
        await update_agent_messages(agent_id, query)
        messages = langgraph_setup.research(query)
            
        return messages[-1] if messages else {"role": "assistant", "content": "No response generated."}
        
    except ValueError as e:
        raise HTTPException(status_code=422, detail=f"Validation error: {str(e)}")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error querying agent: {str(e)}")
