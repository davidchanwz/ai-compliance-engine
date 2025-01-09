from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.core.security import get_password_hash, verify_password
from app.core.jwt import create_access_token
from app.database.db_functions import SessionLocal
from app.database.alembic_models import User
from app.dependencies import get_db
from app.services.user_service import get_user_by_email
import logging


router = APIRouter()

class RegisterRequest(BaseModel):
    email: str
    password: str

class LoginRequest(BaseModel):
    email: str
    password: str

# Set up a logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)  # Set the logging level
handler = logging.StreamHandler()  # Log to the console
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


@router.post("/login")
def login(request: LoginRequest, db: Session = Depends(get_db)):
    logger.info(f"Login attempt for email: {request.email}")
    
    user = get_user_by_email(db, request.email)
    logger.info(f"User fetched: {user}")

    if not user:
        logger.warning(f"Login failed: No user found with email {request.email}")
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    if not verify_password(request.password, user.hashed_password):
        logger.warning(f"Login failed: Incorrect password for user {request.email}")
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    access_token = create_access_token(data={"sub": str(user.id), "email": str(user.email)})
    logger.info(f"Login successful for user {request.email}")
    
    return {"access_token": access_token, "token_type": "bearer"}
