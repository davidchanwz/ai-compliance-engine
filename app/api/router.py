from fastapi import APIRouter
from app.api.endpoints.auth import router as auth_router
from app.api.endpoints.protected import router as protected_router


# Create the main API router
api_router = APIRouter()

# Include specific routers from each endpoint module
api_router.include_router(auth_router)
api_router.include_router(protected_router)