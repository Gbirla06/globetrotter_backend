import random
import json
from fastapi import HTTPException, APIRouter
from app.database import destinations_collection
from app.models import GuessRequest


router = APIRouter(tags=[__name__])

@router.get("")
async def root():
    return {"message": "Welcome to Destination Page"}

@router.get("random")
async def get_random_destination():
    try :
        destinations = await destinations_collection.find().to_list(200)

        if not destinations :
            raise HTTPException(status_code=404, detail="No destination found")
        
        random_destination = random.choice(destinations)

        return {
            "alias": random_destination["alias"],
            "name": random_destination["name"],
            "clues": random.sample(random_destination["clues"], min(2, len(random_destination["clues"]))),
            "funFacts": random.sample(random_destination["funFacts"], min(1, len(random_destination["funFacts"])))
        }
    
    except Exception as e :
        raise HTTPException(status_code=500, detail="Internal Server Error")
    

@router.post("")
async def add_destinations() :
    try :
        with open("globetrotter_dataset_unique_clues.json", "r", encoding="utf-8") as file :
            data = json.load(file)

        count = await destinations_collection.count_documents({})

        for destination in data :
            existing_doc = await destinations_collection.find_one({'name' : destination['name']})
            if existing_doc is None :
                count+=1
                await destinations_collection.insert_one({
                    "alias": f"dst{count}",
                    "name": destination['name'],
                    "clues": destination['clues'],
                    "funFacts": destination['funFacts']
                })
            else :
                await destinations_collection.update_one(
                    {"name": destination["name"]},  # Filter
                    {"$set": {
                        "clues": destination["clues"],
                        "funFacts": destination["funFacts"]
                    }}
                )
        return "!!Data inserted Successfully!!"

    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="File Not found")
    except json.JSONDecodeError as e:
        raise HTTPException(status_code=500, detail="File contain invalid json")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")
        


@router.post("/submit-guess")
async def submit_guess(guess_data: GuessRequest):
    destination = await destinations_collection.find_one({'alias' : guess_data.alias})

    if not destination :
        raise HTTPException(status_code=404, detail="Destination Not Found")
    
