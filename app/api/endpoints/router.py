from fastapi import APIRouter, Depends

from app.api.endpoints.product import router as product_router
from app.core.dependencies.authentication import identify_third_party_request

router = APIRouter(dependencies=[Depends(identify_third_party_request)])

router.include_router(product_router)
