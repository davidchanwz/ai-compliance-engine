from fastapi import APIRouter

# Create the router for health checks
router = APIRouter()

@router.get("/")
async def health_check():
    return {"status": "ok"}