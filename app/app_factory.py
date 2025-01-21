from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.api.middleware import RequestLogMiddleware
from app.api.router import main_api_router
from app.app_lifespan import lifespan
from app.core.config import settings


def create_app():
    """
    Factory responsible for bootstrapping and creating the FastAPI application.
    """

    app = FastAPI(title=settings.APP_TITLE, lifespan=lifespan)

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
