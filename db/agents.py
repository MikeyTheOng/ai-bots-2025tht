from bson.objectid import ObjectId
from db.errors import InvalidAgentIDError
from models.agents import AgentDB, CreateAgent, File as FileModel
from typing import List

async def create_agent(new_agent: CreateAgent):
    """
    Create a new research agent
    
    Args:
        new_agent: Validated CreateAgent model containing agent details
    
    Returns:
        Newly created agent
    """
    try:
        new_agent = AgentDB(name=new_agent.name, files=new_agent.files)
        await new_agent.insert()
        
        return new_agent
    except:
        raise
    
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
            raise InvalidAgentIDError(agent_id)
        agent = await AgentDB.get(agent_id)
        return agent
    except:
        raise
    
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
            raise InvalidAgentIDError(agent_id)
        agent = await AgentDB.get(agent_id)
        if not agent:
            return None
        await agent.delete()
    except:
        raise
    
async def update_agent_files(agent_id: str, new_files: List[FileModel]):
    """
    Append agent files
    
    Args:
        agent_id: ID of the agent to update
        new_files: List of files to append to agent files
    
    Returns:
        Updated agent or None if agent doesn't exist
    """
    try:
        if not ObjectId.is_valid(agent_id):
            raise InvalidAgentIDError(agent_id)
        
        agent = await AgentDB.get(agent_id)
        
        agent.files.extend(new_files)
        
        await agent.save()
        
        return agent
    except:
        raise
    
async def update_agent_messages(agent_id: str, message: str):
    """
    Append agent messages
    
    Args:
        agent_id: ID of the agent to update
        message: Message to append to agent messages
        
    Returns:
        Updated agent or None if agent doesn't exist
    """
    try:
        if not ObjectId.is_valid(agent_id):
            raise InvalidAgentIDError(agent_id)
        
        agent = await AgentDB.get(agent_id)
        
        agent.messages.append(message)
        
        await agent.save()
        
        return agent
    except:
        raise