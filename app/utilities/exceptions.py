from fastapi import HTTPException, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from app.main import app

class CustomHTTPException(HTTPException):
    '''Custom HTTP exception handler class'''
    
    def __init__(self, status_code: int, detail: str, headers: dict = None):
        super().__init__(status_code=status_code, detail=detail, headers=headers)


@app.exception_handler(CustomHTTPException)
async def custom_exception_handler(request: Request, exc: CustomHTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "status": "Bad request",
            "message": exc.detail,
            "status_code": exc.status_code
        }
    )


# Customizing validation exceptions
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Custom validation error handler"""

    # Create an empty errors list
    errors = []

    # Loop through all validation errors that could occur
    for error in exc.errors():
        error_field = error['loc'][-1]
        error_message = error['msg']

        errors.append({
            'field': error_field,
            'message': error_message
        })

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            'errors': errors
        }
    )
