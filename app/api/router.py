from fastapi import APIRouter

from app.api.endpoints.router import router as ep_router

main_api_router = APIRouter()

main_api_router.include_router(ep_router)
