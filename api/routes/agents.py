from api.routes.utils import DefaultErrorMessages, handle_validation_error
from db.agents import create_agent, delete_agent, get_agent, update_agent_files, update_agent_messages, update_agent_websites
from fastapi import APIRouter, File, Form, HTTPException, UploadFile
import json
from langgraph_setup import LangGraphSetup
from llm_setup import LLMSetup
from models.agents import AgentDB, CreateAgent, File as FileModel
from models.messages import Message
from tool_setup import ToolSetup
from typing import Dict, List, Tuple
from utils.document_extractor import DocumentExtractor
from utils.token_manager import TokenManager
import os
import tempfile

router = APIRouter()

token_manager = TokenManager(max_tokens=120000)
document_extractor = DocumentExtractor(token_manager=token_manager)

async def process_files(files: List[UploadFile], initial_tokens: int = 0) -> Tuple[List[FileModel], int]:
    """
    Process uploaded files, extract text and calculate tokens
    
    Args:
        files: List of uploaded files
        initial_tokens: Starting token count (for adding to existing files)
        
    Returns:
        Tuple of (list of processed file records, total token count)
    """
    file_records = []
    current_tokens = initial_tokens
    
    with tempfile.TemporaryDirectory() as temp_dir:
        for file in files:
            file_path = os.path.join(temp_dir, file.filename)
            with open(file_path, "wb") as f:
                f.write(await file.read())
            
            if not document_extractor.is_supported_file(file_path):
                _, ext = os.path.splitext(file_path.lower())
                raise HTTPException(
                    status_code=400, 
                    detail=f"Unsupported file extension: {ext}. Supported types are: {', '.join(document_extractor.SUPPORTED_EXTENSIONS.keys())}"
                )
            
            try:
                text, tokens = document_extractor.extract_from_file(file_path)
            except Exception as e:
                raise HTTPException(status_code=400, detail=f"Error processing file {file.filename}: {str(e)}")
            
            would_exceed, total_tokens = token_manager.check_token_limit(current_tokens, tokens)
            if would_exceed:
                raise HTTPException(
                    status_code=400, 
                    detail=f"Token limit exceeded. Current: {current_tokens}, Additional: {tokens}, Total would be: {total_tokens}, Max: {token_manager.max_tokens}"
                )
            
            current_tokens = total_tokens 
            
            file_records.append(FileModel(
                name=file.filename,
                text=text,
                tokens=tokens
            ))
            
    return file_records, current_tokens

@router.post("/agents", status_code=201, response_model=Dict[str, str])
async def create_agent_route(
    agent_post: str = Form(...),
    files: List[UploadFile] = File([])
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
        file_records, _ = await process_files(files)
        agent_data["files"] = file_records
        
        validated_agent = CreateAgent(**agent_data)
        
        new_agent = await create_agent(validated_agent)
        return {"agent_id": str(new_agent.id)}
    
    except json.JSONDecodeError:
        raise handle_validation_error(ValueError(DefaultErrorMessages.INVALID_JSON_FORMAT))
    except ValueError as e:
        raise handle_validation_error(e)
    except Exception as e:
        raise HTTPException(status_code=500, detail=DefaultErrorMessages.INTERNAL_SERVER_ERROR)
    
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
        location = ["path", "agent_id"] if DefaultErrorMessages.INVALID_AGENT_ID in str(e) else None
        raise handle_validation_error(e, location=location)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=DefaultErrorMessages.INTERNAL_SERVER_ERROR)

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
        location = ["path", "agent_id"] if DefaultErrorMessages.INVALID_AGENT_ID in str(e) else None
        raise handle_validation_error(e, location=location)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=DefaultErrorMessages.INTERNAL_SERVER_ERROR)
    
@router.put("/agents/{agent_id}/websites", status_code=204)
async def update_agent_websites_route(
    agent_id: str,
    websites: List[str]
):
    """
    Extract text from websites specified, populating the agent's website list.
    This is part of the bonus assignment.
    """
    try:
        agent = await get_agent(agent_id)
        if not agent:
            return
        
        current_tokens = sum(file.tokens for file in agent.files)
        current_tokens += sum(website.tokens for website in agent.websites)
        
        website_files = []
        
        for url in websites:
            try:
                if not url.startswith("https"):
                    raise ValueError("URL must start with 'https'")
                text, tokens = document_extractor.extract_from_website(url)
                
                would_exceed, _ = token_manager.check_token_limit(current_tokens, tokens)
                if would_exceed:
                    raise HTTPException(
                        status_code=400,
                        detail=f"Token limit exceeded. Max: {token_manager.max_tokens}"
                    )
                
                website_files.append(FileModel(
                    name=url,
                    text=text,
                    tokens=tokens
                ))
                current_tokens += tokens
            except Exception as e:
                raise HTTPException(
                    status_code=500,
                    detail=f"Failed to extract text from website {url}: {str(e)}"
                )
        
        await update_agent_websites(agent_id, website_files) 
    except ValueError as e:
        raise handle_validation_error(e)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
    
@router.put("/agents/{agent_id}/files", status_code=204)
async def update_agent_files_route(
    agent_id: str,
    files: List[UploadFile]
):
    """
    Extracts text from the files uploaded, populating the agent's file list.
    """
    try:
        agent = await get_agent(agent_id)
        if not agent:
            return
        
        file_records = []
        current_tokens = sum(file.tokens for file in agent.files)
        current_tokens += sum(website.tokens for website in agent.websites)
        
        file_records, new_tokens = await process_files(files, current_tokens)
        
        if current_tokens + new_tokens > token_manager.max_tokens:
            raise HTTPException(
                status_code=400,
                detail=f"Token limit exceeded. Current: {current_tokens}, Additional: {new_tokens}, Total would be: {current_tokens + new_tokens}, Max: {token_manager.max_tokens}"
            )
        
        await update_agent_files(agent_id, file_records)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=DefaultErrorMessages.INTERNAL_SERVER_ERROR)

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
        
        llm_setup = LLMSetup()
        tool_setup = ToolSetup()
        langgraph_setup = LangGraphSetup(llm_setup, tool_setup, agent.files)

        await update_agent_messages(agent_id, query)
        
        messages = langgraph_setup.research(query)
            
        return messages[-1] if messages else {"role": "assistant", "content": "No response generated."}
        
    except ValueError as e:
        location = ["path", "agent_id"] if DefaultErrorMessages.INVALID_AGENT_ID in str(e) else None
        raise handle_validation_error(e, location=location)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=DefaultErrorMessages.INTERNAL_SERVER_ERROR)
