from fastapi import APIRouter, HTTPException, Depends, Header
from fastapi.security import OAuth2PasswordRequestForm

from app.database import find_user, insert_user, get_database
from app.schemas import User
from app.utils import generate_token, username_from_token

router = APIRouter(tags=["users"])


async def _find_user_by_token(token: str = Header(...), db=Depends(get_database)):
    if not token:
        raise HTTPException(status_code=401, detail="Auth Required")
    username = await username_from_token(token)
    if not username:
        raise HTTPException(status_code=401, detail="Cannot find username from token")

    user = await find_user(db, username)
    if not user:
        raise HTTPException(status_code=401, detail="User does not exist")
    return user


@router.post("/users")
async def sign_up(user: User, db=Depends(get_database)):
    exist_user = await find_user(db, user.account_id)
    if exist_user:
        raise HTTPException(status_code=409, detail="user id already existed")
    else:
        result = await insert_user(db, user)
        if result and result.acknowledged:
            return user
        else:
            raise HTTPException(status_code=400, detail="insert new user failed")


@router.post("/users/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db=Depends(get_database)):
    user = await find_user(db, form_data.username)
    if not user or user.password != form_data.password:
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    access_token = await generate_token(user.account_id)
    return {"access_token": access_token}


@router.get("/users/{id}", response_model=User)
async def get_user(id: str, user=Depends(_find_user_by_token)):
    if user.account_id != id:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return user
