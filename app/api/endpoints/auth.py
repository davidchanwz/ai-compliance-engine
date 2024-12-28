from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

# Create the router for authentication
router = APIRouter()

# Request and Response Models
class LoginRequest(BaseModel):
    username: str
    password: str

class LoginResponse(BaseModel):
    access_token: str
    token_type: str

@router.post("/login", response_model=LoginResponse)
async def login(request: LoginRequest):
    # Dummy authentication logic
    if request.username == "admin" and request.password == "password":
        return {"access_token": "fake-jwt-token", "token_type": "bearer"}
    raise HTTPException(status_code=401, detail="Invalid credentials")