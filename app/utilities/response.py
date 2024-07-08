from typing import Any, Optional
from fastapi.responses import JSONResponse

def make_response(status: str, message: str, status_code: int, data: Optional[Any] = None):
    """Returns a JSON response for data specified in function arguments."""

    response = {
        'status': status,
        'message': message
    }
    
    if data is not None:
        response['data'] = data
    
    if status_code not in [200, 201]:
        response['statusCode'] = status_code

    return JSONResponse(content=response, status_code=status_code)
