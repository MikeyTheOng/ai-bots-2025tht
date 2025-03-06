from fastapi import HTTPException

class DefaultErrorMessages:
    """Default error messages used in API routes."""
    
    INVALID_AGENT_ID = "Invalid agent ID format"
    FORBIDDEN = "Access forbidden"
    INVALID_JSON_FORMAT = "Invalid JSON format"
    INTERNAL_SERVER_ERROR = "Internal server error occurred"
    
def handle_validation_error(error, location=None):
    """Convert a ValueError to a structured HTTPException"""
    if location:
        return HTTPException(
            status_code=422,
            detail=[{
                "loc": location,
                "msg": str(error),
                "type": "value_error"
            }]
        )
    return HTTPException(
        status_code=422,
        detail=[{
            "loc": error.location if hasattr(error, "location") else ["input"],
            "msg": str(error),
            "type": "value_error"
        }]
    )