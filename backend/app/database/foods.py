from app.schemas import Food


async def insert_food(db, food: Food):
    doc = await db.foods.insert_one(food.dict())
    return doc


async def find_food(db, food_name):
    doc = await db.foods.find_one({"name": food_name})
    if doc:
        doc.pop("_id", None)
    return Food(**doc) if doc else None


async def find_all_foods(db):
    docs = [doc async for doc in db.foods.find()]
    for doc in docs:
        doc.pop("_id", None)
    foods = [Food(**doc) for doc in docs]
    return foods


async def update_food(db, food: Food):
    doc = await db.foods.replace_one(food.dict())
    return doc


async def delete_food(db, food_name):
    result = await db.foods.delete_many({"name": food_name})
    return result


async def drop_foods(db):
    result = await db.foods.drop()
    return result
