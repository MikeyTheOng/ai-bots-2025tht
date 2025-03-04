import json
import pytest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from bson import ObjectId

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from main import app

client = TestClient(app)

def test_create_agent_success():
    """Test successful agent creation"""
    test_data = {"name": "Test Agent"}
    
    with patch("api.routes.agents.create_agent") as mock_create:
        mock_agent = MagicMock()
        mock_agent.id = ObjectId("507f1f77bcf86cd799439011")
        mock_create.return_value = mock_agent
        
        response = client.post(
            "/agents",
            data={"agent_post": json.dumps(test_data)}
        )
        print("Response:", response.json())

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