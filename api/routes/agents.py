from fastapi import APIRouter, Form, HTTPException
from typing import Dict
import json

from db.agents import create_agent
from models.agents import CreateAgent

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