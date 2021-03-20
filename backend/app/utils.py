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


async def username_from_token(token: str):
    payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    return payload.get("username", None)


async def get_user_by_token(token: str = Header(...), db=Depends(get_database)):
    if not token:
        raise HTTPException(status_code=401, detail="Auth Required")
    username = await username_from_token(token)
    if not username:
        raise HTTPException(status_code=401, detail="Cannot find username from token")

    user = await find_user(db, username)
    if not user:
        raise HTTPException(status_code=401, detail="User does not exist")
    return user
