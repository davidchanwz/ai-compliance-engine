from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

# Create the router for KYC
router = APIRouter()

# Request and Response Models
class KYCRequest(BaseModel):
    user_id: str
    full_name: str
    dob: str
    id_number: str
    id_type: str

class KYCResponse(BaseModel):
    user_id: str
    is_verified: bool

@router.post("/verify", response_model=KYCResponse)
async def verify_kyc(request: KYCRequest):
    # Dummy KYC logic
    is_verified = request.id_number.startswith("A")
    return {"user_id": request.user_id, "is_verified": is_verified}