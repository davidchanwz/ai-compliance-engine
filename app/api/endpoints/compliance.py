from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from requests import Session
from app.dependencies import get_db
from app.services.compliance_service import feature_names, predict_anomaly 

# Create the router for compliance
router = APIRouter()

# Request and Response Models
class TransactionCheckRequest(BaseModel):
    transaction_id: str
    amount: float
    sender_account: str
    receiver_account: str

class TransactionCheckResponse(BaseModel):
    transaction_id: str
    anomalous: bool
    anomaly_score: float

@router.post("/transaction-check", response_model=TransactionCheckResponse)
def transaction_check(request: TransactionCheckRequest, db: Session = Depends(get_db)):
    # Call the prediction logic
    result = predict_anomaly(request.transaction_id, db)
    
    return TransactionCheckResponse(
        transaction_id=request.transaction_id,
        anomalous=result["anomaly"],
        anomaly_score=result["anomaly_rating"]
    )
