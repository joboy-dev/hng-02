from fastapi import FastAPI

from app.app_functions import create_routes, add_middleware

# Create app
app = FastAPI(
    title='HNG Stage 2 Task',
    description='User Authentication and Organisation',
    version='v1',
)

# Add middleware
add_middleware(app)

# Add routes
create_routes(app)
