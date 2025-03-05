import json
from bson import ObjectId
import json
import os
import pytest
import sys
from fastapi.testclient import TestClient
from unittest.mock import MagicMock, patch

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

from main import app

client = TestClient(app)

def test_create_agent_success():
    """Test successful agent creation"""
    test_data = {"name": "Test Agent"}
    
    with patch("api.routes.agents.create_agent") as mock_create:
        mock_agent = MagicMock()
        mock_agent._id = ObjectId("507f1f77bcf86cd799439011")
        mock_create.return_value = mock_agent
        
        response = client.post(
            "/agents",
            data={"agent_post": json.dumps(test_data)}
        )

        assert response.status_code == 201
        assert "agent_id" in response.json()
        assert isinstance(response.json()["agent_id"], str)
        
        mock_create.assert_called_once()

def test_create_agent_invalid_json():
    """Test handling of invalid JSON"""

    response = client.post(
        "/agents",
        data={"agent_post": "{invalid json}"}
    )
    
    assert response.status_code == 422
    assert "Invalid JSON" in response.json()["detail"]

def test_create_agent_missing_required_fields():
    """Test handling of missing required fields"""

    response = client.post(
        "/agents",
        data={"agent_post": "{}"}
    )
    
    assert response.status_code == 422
    assert "Invalid agent data" in response.json()["detail"]

def test_create_agent_database_error():
    """Test handling of database errors"""
    test_data = {"name": "Test Agent"}
    
    with patch("db.agents.create_agent") as mock_create:
        mock_create.side_effect = Exception("Database connection failed")
        
        response = client.post(
            "/agents",
            data={"agent_post": json.dumps(test_data)}
        )
        
        assert response.status_code == 500
        assert "Error creating agent" in response.json()["detail"]

def test_get_agent_success():
    """Test successful agent retrieval"""
    agent_id = "507f1f77bcf86cd799439011"
    
    with patch("api.routes.agents.get_agent") as mock_get:
        mock_agent = MagicMock()
        mock_agent._id = ObjectId(agent_id)
        mock_agent.name = "Test Agent"
        mock_agent.revision_id = "12345678-1234-5678-1234-567812345678"  # Needs to be included as fastAPI validates the mock_agent created via MagicMock against AgentDB model
        mock_get.return_value = mock_agent
        
        response = client.get(f"/agents/{agent_id}")
        
        assert response.status_code == 200
        assert response.json()["name"] == "Test Agent"
        assert "_id" in response.json()
        
        mock_get.assert_called_once_with(agent_id)

def test_get_agent_not_found():
    """Test agent not found case"""
    agent_id = "507f1f77bcf86cd799439011"
    
    with patch("api.routes.agents.get_agent") as mock_get:
        mock_null_agent = MagicMock()
        mock_null_agent._id = None
        mock_null_agent.name = ""
        mock_null_agent.revision_id = "12345678-1234-5678-1234-567812345678"
        mock_get.return_value = mock_null_agent
        
        response = client.get(f"/agents/{agent_id}")
        assert response.status_code == 200
        assert response.json()["name"] == ""
        assert response.json()["_id"] is None
        
        mock_get.assert_called_once_with(agent_id)

def test_get_agent_validation_error():
    """Test validation error handling"""
    agent_id = "invalid-id"
    
    with patch("api.routes.agents.get_agent") as mock_get:
        mock_get.side_effect = ValueError("Invalid agent ID format")
        
        response = client.get(f"/agents/{agent_id}")
        
        assert response.status_code == 422
        assert "Validation error" in response.json()["detail"]
        
        mock_get.assert_called_once_with(agent_id)

def test_delete_agent_success():
    """Test successful agent deletion"""
    agent_id = "507f1f77bcf86cd799439011"
    
    with patch("api.routes.agents.delete_agent") as mock_delete:
        mock_delete.return_value = None
        
        response = client.delete(f"/agents/{agent_id}")
        
        assert response.status_code == 204
        assert response.content == b''
        
        mock_delete.assert_called_once_with(agent_id)

def test_delete_agent_validation_error():
    """Test validation error handling during deletion"""
    agent_id = "invalid-id"
    
    with patch("api.routes.agents.delete_agent") as mock_delete:
        mock_delete.side_effect = ValueError("Invalid agent ID format")
        
        response = client.delete(f"/agents/{agent_id}")
        
        assert response.status_code == 422
        assert "Validation error" in response.json()["detail"]
        
        mock_delete.assert_called_once_with(agent_id)

class TestAgentQueriesRoute:
    @pytest.fixture
    def mock_research_results(self):
        """Create mock research results"""
        return [
            {"role": "user", "content": "What is climate change?"},
            {"role": "assistant", "content": "Climate change refers to long-term shifts in temperatures and weather patterns. [https://example.org/climate]"}
        ]
    
    @patch("api.routes.agents.langgraph_setup.research")
    def test_send_message_success(self, mock_research, mock_research_results):
        """Test successful message sending"""
        mock_research.return_value = mock_research_results
        
        agent_id = str(ObjectId())
        message = {"message": "What is climate change?"}
        
        response = client.post(f"/agents/{agent_id}/queries", json=message)
        
        assert response.status_code == 201
        
        mock_research.assert_called_once_with("What is climate change?")
        
        assert response.json() == mock_research_results[-1]
    
    @patch("api.routes.agents.langgraph_setup.research")
    def test_send_message_research_error(self, mock_research):
        """Test handling of research errors"""
        mock_research.side_effect = Exception("Research error")
        
        agent_id = str(ObjectId())
        message = {"message": "What is climate change?"}
        
        response = client.post(f"/agents/{agent_id}/queries", json=message)
        
        assert response.status_code == 500
        assert "Error querying agent" in response.json()["detail"]
    
    @patch("api.routes.agents.langgraph_setup.research")
    def test_empty_research_results(self, mock_research):
        """Test handling of empty research results"""
        mock_research.return_value = []
        
        agent_id = str(ObjectId())
        message = {"message": "What is climate change?"}
        
        response = client.post(f"/agents/{agent_id}/queries", json=message)
        
        assert response.status_code == 201
        assert response.json() == {"role": "assistant", "content": "No response generated."}
    
    @patch("api.routes.agents.langgraph_setup.research")
    def test_validation_error(self, mock_research):
        """Test handling of validation errors"""
        mock_research.side_effect = ValueError("Invalid message format")
        
        agent_id = str(ObjectId())
        message = {"message": "What is climate change?"}
        
        response = client.post(f"/agents/{agent_id}/queries", json=message)
        
        assert response.status_code == 422
        assert "Validation error" in response.json()["detail"]