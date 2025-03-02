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
    username = username.lower()
    user = await users_collection.find_one({'username' : username})
    if user :
        return {'is_exist': True, 'username' : username, 'score' : user['score'], 'correct_score' : user['correct_score'], 'incorrect_score' : user['incorrect_score'], 'total_referrals' : len(user['challenges'])} 
    
    users_collection.insert_one({
        "is_exist"  : False,
        "username" : username,
        "score" : 0,
        "correct_score" : 0,
        "incorrect_score" : 0,
        "challenges" : []
    })

    return {'username' : username, 'score' : 0, 'correct_score' : 0, 'incorrect_score' : 0, 'total_referrals' : 0} 


# @router.post("/challenge")
# async def challenge_friend(challenger_username: str, friend_username: str):
#     challenger_username = challenger_user.lower()
#     friend_username = friend_username.lower()
#     challenger_user = await users_collection.find_one({'username' : challenger_username})

#     if challenger_user is None :
#         raise HTTPException(status_code=404, detail="Challenger not found")
    
#     friend_user = await users_collection.find_one({'username' : friend_username})

#     if friend_user :
#         raise HTTPException(status_code=404, detail="User already exist")
    
#     challenge_entry = {
#         "friend" : friend_username,
#         "timestamp" : datetime.now()
#     }

#     users_collection.update_one(
#         {"username" : challenger_username},
#         {"$push" : {"challenges" : challenge_entry}}
#     )

#     share_link = f"{APPLICATION_URL}/play?challenge_id={friend_username}"

#     return {"message": "Challenge sent!", "share_link": share_link}
