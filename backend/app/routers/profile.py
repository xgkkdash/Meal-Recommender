from fastapi import APIRouter, HTTPException, Depends, Header

from app.database import get_database
from app.database.users import find_user, update_user
from app.schemas import User
from app.utils import username_from_token

router = APIRouter(tags=["profile"])


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


@router.get("/profile", response_model=User)
async def get_profile(user=Depends(_find_user_by_token)):
    return user


@router.put("/profile", response_model=User)
async def update_profile(target_user: User, current_user=Depends(_find_user_by_token), db=Depends(get_database)):
    if target_user.account_id != current_user.account_id:
        raise HTTPException(status_code=401, detail="Cannot change account_id")
    result = await update_user(db, target_user)
    if result:
        return target_user
    raise HTTPException(status_code=500, detail="Update profile failed")
