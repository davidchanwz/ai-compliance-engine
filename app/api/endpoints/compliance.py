from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from app.dependencies import get_current_user
from requests import Session
from app.dependencies import get_db
from app.database.alembic_models import User  # Replace with your actual User model
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

@router.post("/transaction-check", response_model=TransactionCheckResponse)
async def transaction_check(request: TransactionCheckRequest, db: Session = Depends(get_db), current_user: User = Depends(get_current_user),  # Protect the endpoint
):
    # Call the prediction logic
    result = predict_anomaly(request.transaction_id, db)
    
    return TransactionCheckResponse(
        transaction_id=request.transaction_id,
        anomalous=result["anomaly"],
        anomaly_score=result["anomaly_rating"]
    )