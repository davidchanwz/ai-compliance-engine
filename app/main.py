from fastapi import FastAPI
from app.api.router import api_router
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse

# Initialize the FastAPI app
app = FastAPI(
    title="AI Compliance Engine",
    description="API for Compliance and Risk Management using AI",
    version="1.0.0",
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