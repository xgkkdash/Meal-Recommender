from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm

from app.database import get_database
from app.database.users import find_user, insert_user
from app.schemas import User
from app.utils import generate_token

router = APIRouter(tags=["login"])


@router.post("/register")
async def register(user: User, db=Depends(get_database)):
    exist_user = await find_user(db, user.account_id)
    if exist_user:
        raise HTTPException(status_code=409, detail="user id already existed")
    else:
        result = await insert_user(db, user)
        if result and result.acknowledged:
            return user
        else:
            raise HTTPException(status_code=400, detail="insert new user failed")


@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db=Depends(get_database)):
    user = await find_user(db, form_data.username)
    if not user or user.password != form_data.password:
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    access_token = await generate_token(user.account_id)
    return {"access_token": access_token}
