# app/services/user_service.py
from app.database.alembic_models import User
from sqlalchemy.orm import Session

def get_user_by_email(db: Session, email: str) -> User:
    return db.query(User).filter(User.email == email).first()
