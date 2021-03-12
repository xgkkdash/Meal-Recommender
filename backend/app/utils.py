import jwt

from datetime import datetime, timedelta
from app.config import settings


async def generate_token(username: str):
    to_encode = {"username": username, "exp": datetime.utcnow() + timedelta(minutes=settings.TOKEN_EXPIRE_MINUTES)}
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


async def username_from_token(token: str):
    payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    return payload.get("username", None)
