from fastapi import APIRouter, Header, HTTPException

from app.database import find_user, database
from app.schemas import User
from app.utils import username_from_token

router = APIRouter(
    tags=["items"],
    responses={404: {"description": "Not found"}}
)


@router.get("/")
def root():
    return "Welcome to Meal_Recommender!"


@router.get("/users/me", response_model=User)
async def get_self_data(token: str = Header(...)):
    if not token:
        raise HTTPException(status_code=401, detail="Auth Required")
    username = await username_from_token(token)
    if not username:
        raise HTTPException(status_code=401, detail="Cannot find username from token")

    user = await find_user(database, username)
    if not user:
        raise HTTPException(status_code=401, detail="User does not exist")
    return user
