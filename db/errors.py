class InvalidObjectIdError(ValueError):
    """Custom exception for invalid object IDs."""
    def __init__(self, object_id=None, message=None, location=None):
        self.object_id = object_id
        self.message = message or f"Invalid object ID: {object_id}" if object_id else "Invalid object ID"
        self.location = location or ["input"]
        super().__init__(self.message)

class InvalidAgentIDError(InvalidObjectIdError):
    """Custom exception for invalid agent IDs."""
    def __init__(self, agent_id=None, message=None, location=None):
        default_location = location or ["input", "agent_id"]
        default_message = f"Invalid agent ID format: {agent_id}" if agent_id else "Invalid agent ID format"
        super().__init__(
            object_id=agent_id, 
            message=message or default_message,
            location=default_location
        )