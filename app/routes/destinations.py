import random
import json
import os
from typing import List
from fastapi import HTTPException, APIRouter
from app.database import destinations_collection, users_collection
from app.schema import Destination, GuessRequest
from bson.objectid import ObjectId
from pymongo import ReturnDocument

# Get the flag to allow user to add data from environment variables, default to False if not set
USER_ALLOW_TO_ADD_DATA = os.getenv("USER_ALLOW_TO_ADD_DATA", False)

# Create a new APIRouter instance with a tag for the module name
router = APIRouter(tags=[__name__])

@router.get("")
async def root():
    """
    Root Route
    Returns a welcome message for the Destination Page.
    """
    return {"message": "Welcome to Destination Page"}

@router.get("/random")
async def get_random_destination():
    """
    Get a random destination.
    
    Returns:
    - A dictionary containing the destination ID, clues, and options.
    
    Raises:
    - HTTPException: If no destination is found or an internal server error occurs.
    """
    try:
        random_destination = await destinations_collection.aggregate([{"$sample": {"size": 4}}]).to_list(4)

        if not random_destination:
            raise HTTPException(status_code=404, detail="No destination found")
        
        clues = random_destination[0]['clues']
        id = str(random_destination[0]['_id'])
        random.shuffle(random_destination)
        options = [destination['city'] for destination in random_destination]

        return {
            "id": id,
            "clues": clues,
            "options": options
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.post("")
async def add_destinations(in_data: List[Destination]):
    """
    Add new destinations.
    
    Parameters:
    - in_data: List[Destination] - A list of destinations to add.
    
    Returns:
    - A success message if data is inserted successfully or a message indicating that the user is not allowed to insert data.
    
    Raises:
    - HTTPException: If the file is not found, contains invalid JSON, or an internal server error occurs.
    """
    try:
        # Commented this portion, not required anymore, now onwards we add data using input
        # with open("cities_data.json", "r", encoding="utf-8") as file:
        #     data = json.load(file)

        if USER_ALLOW_TO_ADD_DATA:
            for destination in in_data:
                existing_doc = await destinations_collection.find_one({'city': destination['city']})
                if existing_doc is None:
                    await destinations_collection.insert_one({
                        "city": destination['city'],
                        "country": destination['country'],
                        "clues": destination['clues'],
                        "fun_fact": destination['fun_fact'],
                        "trivia": destination['trivia']
                    })

            return "Data inserted Successfully!!"
        else:
            return "You are not allowed to insert data. Thank You"

    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="File Not found")
    except json.JSONDecodeError as e:
        raise HTTPException(status_code=500, detail="File contains invalid JSON")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.post("/submit-guess")
async def submit_guess(guess_data: GuessRequest):
    """
    Submit a guess for a destination.
    
    Parameters:
    - guess_data: GuessRequest - The guess data containing the destination ID and user's guess.
    
    Returns:
    - A dictionary containing the result of the guess, including fun facts, trivia, and updated user scores.
    
    Raises:
    - HTTPException: If the destination or user is not found.
    """
    destination = await destinations_collection.find_one({'_id': ObjectId(guess_data.id)})

    if not destination:
        raise HTTPException(status_code=404, detail="Destination Not Found")
    
    guess_data.username = guess_data.username.lower()
    result = {}
    result['fun_fact'] = destination['fun_fact']
    result['trivia'] = destination['trivia']
    result['username'] = guess_data.username
    if destination['city'] != guess_data.user_guess:
        user = await users_collection.find_one_and_update(
            {"username": guess_data.username},  
            {"$inc": {"score": -1, "incorrect_score": 1}},
            return_document=ReturnDocument.AFTER
        )

        if not user:
            raise HTTPException(status_code=404, detail="Invalid User ID")
        
        result['score'] = user['score']
        result['correct_score'] = user['correct_score']
        result['incorrect_score'] = user['incorrect_score']
        result['is_guess_right'] = False
        return result
    
    user = await users_collection.find_one_and_update(
        {"username": guess_data.username},  
        {"$inc": {"score": 1, "correct_score": 1}},
        return_document=ReturnDocument.AFTER
    )

    if not user:
        raise HTTPException(status_code=404, detail="Invalid User ID")
    
    result['score'] = user['score']
    result['correct_score'] = user['correct_score']
    result['incorrect_score'] = user['incorrect_score']
    result['is_guess_right'] = True
    return result
