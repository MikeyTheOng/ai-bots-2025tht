from db.agents import create_agent, get_agent
from fastapi import APIRouter, Form, HTTPException
from models.agents import AgentDB, CreateAgent
from typing import Dict
import json

router = APIRouter()

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
