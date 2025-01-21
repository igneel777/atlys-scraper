from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.core.config import settings

from app.api.router import main_api_router
from app.api.middleware import RequestLogMiddleware


def create_app():
    """
    Factory responsible for bootstrapping and creating the FastAPI application.
    """

    app = FastAPI(title=settings.APP_TITLE)


    app.include_router(main_api_router)
    
    app.add_middleware(RequestLogMiddleware)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return app
