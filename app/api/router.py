from fastapi import APIRouter
from app.api.endpoints import auth, compliance, kyc, health

# Create the main API router
api_router = APIRouter()

# Include specific routers from each endpoint module
api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(compliance.router, prefix="/compliance", tags=["Compliance"])
api_router.include_router(kyc.router, prefix="/kyc", tags=["KYC"])
api_router.include_router(health.router, prefix="/health", tags=["Health Check"])