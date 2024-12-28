from fastapi import FastAPI
from app.api.router import api_router

# Initialize the FastAPI app
app = FastAPI(
    title="AI Compliance Engine",
    description="API for Compliance and Risk Management using AI",
    version="1.0.0",
)

# Include the API router
app.include_router(api_router)

# Run the app if executed directly
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)