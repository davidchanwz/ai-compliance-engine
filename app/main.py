from fastapi import FastAPI
from app.api.router import api_router
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware


# Initialize the FastAPI app
app = FastAPI(
    title="AI Compliance Engine",
    description="API for Compliance and Risk Management using AI",
    version="1.0.0",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://ai-compliance-engine.vercel.app"],  
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

# Include the API router
app.include_router(api_router)
app.mount("/ui", StaticFiles(directory="ui"), name="ui")
@app.get("/")

async def redirect_to_ui():
    return RedirectResponse(url="/ui/index.html")

# Run the app if executed directly
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)