from fastapi import FastAPI, HTTPException, Request
from app.routes.destinations import router as destinations_router
from app.routes.users import router as users_router
from app.database import database
from fastapi.middleware.cors import CORSMiddleware

# Create a new FastAPI instance
app = FastAPI()

# Add CORS middleware to allow cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change this to your frontend URL for security
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
async def health_check():
    """
    Health Check Route
    Checks the connection status to the MongoDB database.
    
    Returns:
    - A dictionary containing the connection status and a message.
    """
    try:
        await database.command("ping")
        return {"status": "connected", "message": "MongoDB is connected!"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

# Include routes for destinations and users
app.include_router(destinations_router, prefix="/destination")
app.include_router(users_router, prefix="/user")