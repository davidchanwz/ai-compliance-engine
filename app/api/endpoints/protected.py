from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBearer
from app.core.jwt import verify_access_token
from app.dependencies import get_current_user
from app.database.alembic_models import User
import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
router = APIRouter()
security = HTTPBearer()

@router.get("/protected")
def protected_route(user: User = Depends(get_current_user)):
    # Log user details or any relevant info
    logger.info(f"Protected route accessed by user: {user.email}")
    
    return {"message": f"Welcome, {user.email}!"}
