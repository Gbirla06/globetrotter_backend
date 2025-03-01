from fastapi import FastAPI, APIRouter


router = APIRouter(tags=[__name__])

@router.get("")
async def root():
    return {"message": "Welcome to User Page"}
