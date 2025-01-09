from fastapi import Depends, HTTPException, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.core.jwt import verify_access_token  # Import your JWT utility
from app.services.user_service import get_user_by_email
from sqlalchemy.orm import Session
from app.database.db_functions import SessionLocal
security = HTTPBearer()

# Dependency to get a database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security), 
    db=Depends(get_db)
):
    token = credentials.credentials
    try:
        payload = verify_access_token(token)
        user_email = payload.get("email")
        if user_email is None:
            raise HTTPException(status_code=401, detail="Invalid token")
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))

    user = get_user_by_email(db, user_email)
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")
    
    # Log the user object or any relevant info
    logger.info(f"User fetched in get_current_user: {user}")

    return user

