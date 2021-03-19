from fastapi import APIRouter, HTTPException, Depends

from app.database import get_database
from app.database.users import find_all_users, find_user, delete_user
from app.utils import get_user_by_token

router = APIRouter(tags=["users"])


@router.get("/users")
async def get_all_users(user=Depends(get_user_by_token), db=Depends(get_database)):
    if user.role != "admin":
        raise HTTPException(status_code=401, detail="Unauthorized")
    all_users = await find_all_users(db)
    if not all_users:
        raise HTTPException(status_code=400, detail="Not Found")
    return all_users


@router.get("/users/{account_id}")
async def get_user(account_id: str, user=Depends(get_user_by_token), db=Depends(get_database)):
    if user.role != "admin":
        raise HTTPException(status_code=401, detail="Unauthorized")
    target_user = await find_user(db, account_id)
    if not target_user:
        raise HTTPException(status_code=400, detail="Not Found")
    return target_user


@router.delete("/users/{account_id}")
async def remove_user(account_id: str, user=Depends(get_user_by_token), db=Depends(get_database)):
    if user.role != "admin":
        raise HTTPException(status_code=401, detail="Unauthorized")
    await delete_user(db, account_id)
    return {"success": True}
