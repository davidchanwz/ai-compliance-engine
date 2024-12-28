from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

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
    is_compliant: bool
    risk_score: float

@router.post("/transaction-check", response_model=TransactionCheckResponse)
async def transaction_check(request: TransactionCheckRequest):
    # Dummy compliance logic
    risk_score = 0.1 if request.amount < 1000 else 0.8
    is_compliant = risk_score < 0.5
    return {
        "transaction_id": request.transaction_id,
        "is_compliant": is_compliant,
        "risk_score": risk_score,
    }