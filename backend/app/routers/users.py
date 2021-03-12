from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm

from app.database import find_user, insert_user, database
from app.schemas import User
from app.utils import generate_token

router = APIRouter(
    tags=["users"],
    responses={404: {"description": "Not found"}}
)


@router.post("/signup")
async def sign_up(user: User):
    exist_user = await find_user(database, user.account_id)
    if exist_user:
        raise HTTPException(status_code=409, detail="user id already existed")
    else:
        result = await insert_user(database, user)
        if result and result.acknowledged:
            return user
        else:
            raise HTTPException(status_code=400, detail="insert new user failed")


@router.post("/login")
async def user_login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await find_user(database, form_data.username)
    if not user or user.password != form_data.password:
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    access_token = await generate_token(user.account_id)
    return {"access_token": access_token}
