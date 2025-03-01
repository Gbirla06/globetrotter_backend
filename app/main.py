from fastapi import FastAPI, HTTPException, Request
from app.routes.destinations import router as destinations_router
from app.routes.users import router as users_router
from app.routes.play import router as play_router
from app.database import database

app = FastAPI()

@app.get("/health")
async def health_check():
    try :
        await database.command("ping")
        return {"status": "connected", "message": "MongoDB is connected!"}
    except Exception as e:
        return {"status": "error", "message": str(e)}
    

    
# Include routes
app.include_router(destinations_router, prefix="/destination")
app.include_router(users_router, prefix="/user" )
app.include_router(play_router, prefix="/play")