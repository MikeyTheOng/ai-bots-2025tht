from fastapi import HTTPException

def handle_validation_error(error):
    """Convert a ValueError to a structured HTTPException"""
    location = error.location if hasattr(error, "location") else ["input"]
    return HTTPException(
        status_code=422,
        detail=[{
            "loc": location,
            "msg": str(error),
            "type": "value_error"
        }]
    )