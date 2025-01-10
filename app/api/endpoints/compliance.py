import datetime
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import UUID
from app.dependencies import get_current_user
from requests import Session
from app.dependencies import get_db
from app.database.alembic_models import AuditTrail, User  # Replace with your actual User model
from app.services.compliance_service import feature_names, predict_anomaly 

# Create the router for compliance
router = APIRouter()

# Request and Response Models
class TransactionCheckRequest(BaseModel):
    transaction_id: str

class TransactionCheckResponse(BaseModel):
    transaction_id: str
    anomalous: bool
    anomaly_score: float

class AuditTrailSchema(BaseModel):
    id: UUID
    timestamp: datetime
    user_id: UUID
    action: str
    transaction_id: str | None
    details: str | None
    class Config: 
        orm_mode = True
        arbitrary_types_allowed = True


@router.get("/audit-trail", response_model=List[AuditTrailSchema])
async def get_audit_trail(
    db: Session = Depends(get_db), 
    current_user=Depends(get_current_user),
):
    # Fetch logs, optionally filter by user or action
    logs = db.query(AuditTrail).filter_by(user_id=current_user.id).all()
    return logs

@router.post("/transaction-check", response_model=TransactionCheckResponse)
async def transaction_check(request: TransactionCheckRequest, db: Session = Depends(get_db), current_user: User = Depends(get_current_user),  # Protect the endpoint
):
    # Call the prediction logic
    result = predict_anomaly(request.transaction_id, db)

    # Save the audit log
    audit_entry = AuditTrail(
        user_id=current_user.id,
        action="TRANSACTION_CHECK",
        transaction_id=request.transaction_id,
        details=f"Input: {request.dict()}, Result: compliant={result['anomaly']}, risk_score={result['anomaly_rating']}",
    )
    db.add(audit_entry)
    db.commit()
    
    return TransactionCheckResponse(
        transaction_id=request.transaction_id,
        anomalous=result["anomaly"],
        anomaly_score=result["anomaly_rating"]
    )