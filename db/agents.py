from bson.objectid import ObjectId
from fastapi import HTTPException
from models.agents import AgentDB, CreateAgent

async def create_agent(new_agent: CreateAgent):
    """
    Create a new research agent
    
    Args:
        new_agent: Validated CreateAgent model containing agent details
    
    Returns:
        Newly created agent
    """
    try:
        new_agent = AgentDB(name=new_agent.name)
        await new_agent.insert()
        
        return new_agent
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating agent: {str(e)}")
    
async def get_agent(agent_id: str):
    """
    Get a research agent by ID
    
    Args:
        agent_id: ID of the agent to retrieve
    
    Returns:
        Agent details or None if not found
    """
    try:
        if not ObjectId.is_valid(agent_id):
            raise HTTPException(status_code=422, detail="Invalid agent ID format")
        agent = await AgentDB.get(agent_id)
        return agent
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving agent: {str(e)}")
    
async def delete_agent(agent_id: str):
    """
    Delete a research agent by ID

    Args:
        agent_id: ID of the agent to delete

    Returns:
        Deleted agent or None if not found
    """
    try:
        if not ObjectId.is_valid(agent_id):
            raise HTTPException(status_code=422, detail="Invalid agent ID format")
        agent = await AgentDB.get(agent_id)
        if not agent:
            return None
        await agent.delete()
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting agent: {str(e)}")