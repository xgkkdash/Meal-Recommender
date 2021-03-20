import jwt

from datetime import datetime, timedelta

from fastapi import Header, Depends, HTTPException

from app.config import settings
from app.database import get_database
from app.database.users import find_user
from app.schemas import UserRole


async def generate_token(user_role: UserRole):
    to_encode = {"username": user_role.user_id, "role": user_role.role_name,
                 "exp": datetime.utcnow() + timedelta(minutes=settings.TOKEN_EXPIRE_MINUTES)}
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


async def user_role_from_token(token: str):
    payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    user_name = payload.get("username", None)
    role = payload.get("role", None)
    return UserRole(user_id=user_name, role_name=role) if user_name and role else None


async def get_user_by_token(token: str = Header(...), db=Depends(get_database)):
    if not token:
        raise HTTPException(status_code=401, detail="Auth Required")
    user_role = await user_role_from_token(token)
    if not user_role:
        raise HTTPException(status_code=401, detail="Invalid token")

    user = await find_user(db, user_role.user_id)
    if not user:
        raise HTTPException(status_code=401, detail="User does not exist")
    return user
