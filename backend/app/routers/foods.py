from fastapi import APIRouter, HTTPException, Depends

from app.database import get_database
from app.database.foods import find_all_foods, find_food, delete_food, insert_food, update_food
from app.schemas import Food
from app.utils import get_user_by_token

router = APIRouter(tags=["foods"])


@router.get("/foods")
async def get_all_foods(user=Depends(get_user_by_token), db=Depends(get_database)):
    all_foods = await find_all_foods(db)
    if not all_foods:
        raise HTTPException(status_code=400, detail="Not Found")
    return all_foods


@router.get("/foods/{name}")
async def get_food(name: str, user=Depends(get_user_by_token), db=Depends(get_database)):
    food = await find_food(db, name)
    if not food:
        raise HTTPException(status_code=400, detail="Not Found")
    return food


@router.post("/foods")
async def create_food(food: Food, user=Depends(get_user_by_token), db=Depends(get_database)):
    if user.role != "admin":
        raise HTTPException(status_code=401, detail="Unauthorized")
    exist_food = await find_food(db, food.name)
    if exist_food:
        raise HTTPException(status_code=409, detail="food name already existed")
    result = await insert_food(db, food)
    if result and result.acknowledged:
        return food
    raise HTTPException(status_code=500, detail="insert new food failed")


@router.put("/foods/{name}")
async def update_food(name: str, food: Food, user=Depends(get_user_by_token), db=Depends(get_database)):
    if user.role != "admin":
        raise HTTPException(status_code=401, detail="Unauthorized")
    exist_food = await find_food(db, name)
    if not exist_food:
        raise HTTPException(status_code=404, detail="food not found, cannot update")
    result = await update_food(db, food)
    if result:
        return food
    raise HTTPException(status_code=500, detail="Update food failed")


@router.delete("/foods/{name}")
async def remove_food(name: str, user=Depends(get_user_by_token), db=Depends(get_database)):
    if user.role != "admin":
        raise HTTPException(status_code=401, detail="Unauthorized")
    await delete_food(db, name)
    return {"success": True}
