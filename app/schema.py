from typing import List
from pydantic import BaseModel


class Destination(BaseModel):
    alias : str
    name : str
    clues : List[str]
    funFacts : List[str]

class GuessRequest(BaseModel):
    alias: str  
    guess: str   
