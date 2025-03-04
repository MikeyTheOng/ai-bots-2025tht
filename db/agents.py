from models.agents import AgentDB, CreateAgent
from fastapi import HTTPException

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