from fastapi import APIRouter

from .api.endpoints import info

api_router = APIRouter()
api_router.include_router(info.router, prefix="/info")
