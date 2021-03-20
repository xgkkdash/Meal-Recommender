from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm

from app.database import get_database
from app.database.users import find_user, insert_user
from app.database.user_roles import insert_user_role, find_user_role
from app.schemas import User, UserRole
from app.utils import generate_token

router = APIRouter(tags=["login"])


@router.post("/register")
async def register(user: User, db=Depends(get_database)):
    exist_user = await find_user(db, user.account_id)
    if exist_user:
        raise HTTPException(status_code=409, detail="user id already existed")
    default_user_role = UserRole(user_id=user.account_id, role_name="regular")
    new_user_result = await insert_user(db, user)
    new_user_role_result = await insert_user_role(db, default_user_role)
    if new_user_result and new_user_result.acknowledged and new_user_role_result and new_user_role_result.acknowledged:
        return user
    raise HTTPException(status_code=500, detail="insert new user failed")


@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db=Depends(get_database)):
    user = await find_user(db, form_data.username)
    if not user or user.password != form_data.password:
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    default_user_role = UserRole(user_id=user.account_id, role_name="regular")
    access_token = await generate_token(default_user_role)
    return {"access_token": access_token}


@router.post("/login/admin")
async def admin_login(form_data: OAuth2PasswordRequestForm = Depends(), db=Depends(get_database)):
    user = await find_user(db, form_data.username)
    if not user or user.password != form_data.password:
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    user_role = UserRole(user_id=user.account_id, role_name="admin")
    if not await find_user_role(db, user_role):
        raise HTTPException(status_code=403, detail="Forbidden for non-admin users")
    access_token = await generate_token(user_role)
    return {"access_token": access_token}
