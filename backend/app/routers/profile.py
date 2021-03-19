from fastapi import APIRouter, HTTPException, Depends

from app.database import get_database
from app.database.users import update_user
from app.schemas import User
from app.utils import get_user_by_token

router = APIRouter(tags=["profile"])


@router.get("/profile", response_model=User)
async def get_profile(user=Depends(get_user_by_token)):
    return user


@router.put("/profile", response_model=User)
async def update_profile(target_user: User, current_user=Depends(get_user_by_token), db=Depends(get_database)):
    if target_user.account_id != current_user.account_id:
        raise HTTPException(status_code=401, detail="Cannot change account_id")
    result = await update_user(db, target_user)
    if result:
        return target_user
    raise HTTPException(status_code=500, detail="Update profile failed")
