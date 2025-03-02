from typing import List
from pydantic import BaseModel

class Destination(BaseModel):
    """
    Schema for a destination.
    
    Attributes:
    - city: str - The name of the city.
    - country: str - The name of the country.
    - clues: List[str] - A list of clues related to the destination.
    - fun_fact: List[str] - A list of fun facts about the destination.
    - trivia: List[str] - A list of trivia questions about the destination.
    """
    city: str
    country: str
    clues: List[str]
    fun_fact: List[str]
    trivia: List[str]

class GuessRequest(BaseModel):
    """
    Schema for a guess request.
    
    Attributes:
    - id: str - The ID of the destination.
    - username: str - The username of the user making the guess.
    - user_guess: str - The user's guess for the destination.
    """
    id: str  
    username: str
    user_guess: str
