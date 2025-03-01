from typing import List
from pydantic import BaseModel


class Destination(BaseModel):
    city: str
    country: str
    clues: List[str]
    fun_fact: List[str]
    trivia: List[str]

class GuessRequest(BaseModel):
    alias: str  
    guess: str   
