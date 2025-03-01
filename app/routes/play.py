from fastapi import APIRouter, HTTPException, Request


router = APIRouter(tags=[__name__])

@router.get("")
async def play_game(request: Request):
    challenge_id = request.query_params.get("challenge_id")
    if not challenge_id:
        raise HTTPException(status_code=400, detail="Invalid challenge link")

    return {"message": "Game started!", "challenge_id": challenge_id}