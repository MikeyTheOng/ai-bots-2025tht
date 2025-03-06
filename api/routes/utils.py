from fastapi import HTTPException

def handle_validation_error(error, location=["input"]):
    """Convert a ValueError to a structured HTTPException"""
    return HTTPException(
        status_code=422,
        detail=[{
            "loc": location,
            "msg": str(error),
            "type": "value_error"
        }]
    )