import os
from fastapi import APIRouter, HTTPException
from app.database import users_collection
from uuid import uuid4
from datetime import datetime

router = APIRouter(tags=[__name__])

APPLICATION_URL = os.getenv("APPLICATION_URL", False)

@router.get("")
async def root():
    return {"message": "Welcome to User Page"}


@router.post("/register")
async def register_user(username : str) :
    user = await users_collection.find_one({'username' : username})
    if user :
        raise HTTPException(status_code=400, detail="username already exists")
    
    users_collection.insert_one({
        "username" : username,
        "score" : 0,
        "challenges" : []
    })

    return {"message": "User registered successfully!"}


@router.post("/challenge")
async def challenge_friend(challenger_username: str, friend_username: str):
    challenger_user = await users_collection.find_one({'username' : challenger_username})

    if challenger_user is None :
        raise HTTPException(status_code=404, detail="Challenger not found")
    
    challenge_Id = str(uuid4())
    challenge_entry = {
        "friend" : friend_username,
        "status" : "pending",
        "timestamp" : datetime.now()
    }

    users_collection.update_one(
        {"username" : challenger_username},
        {"$push" : {"challenges" : challenge_entry}}
    )

    share_link = f"{APPLICATION_URL}/play?challenge_id={challenge_Id}"

    return {"message": "Challenge sent!", "share_link": share_link}
