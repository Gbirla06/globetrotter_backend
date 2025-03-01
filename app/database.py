from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = "globetrotter"

client = AsyncIOMotorClient(MONGO_URI)
database = client[DB_NAME]
destinations_collection = database["destinations"]
users_collection = database["users"]
