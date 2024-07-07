from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


def create_routes(app: FastAPI):
    '''Creates all routes'''

    from app.api.user.auth_routes import auth_router
    from app.api.user.routes import user_router
    from app.api.organisation.routes import org_router

    app.include_router(auth_router)
    app.include_router(user_router)
    app.include_router(org_router)


def add_middleware(app: FastAPI):
    '''Adds middleware to the app'''

    app.add_middleware(
        CORSMiddleware,
        allow_origins=['*'],
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*']
    )
