from app.schemas import User


async def insert_user(db, user: User):
    doc = await db.users.insert_one(user.dict())
    return doc


async def find_user(db, user_id):
    doc = await db.users.find_one({"account_id": user_id})
    if doc:
        doc.pop("_id", None)
    return User(**doc) if doc else None


async def find_all_users(db):
    docs = [doc async for doc in db.users.find()]
    for doc in docs:
        doc.pop("_id", None)
    users = [User(**doc) for doc in docs]
    return users


async def update_user(db, user: User):
    doc = await db.users.replace_one(user.dict())
    return doc


async def delete_user(db, user_id):
    result = await db.users.delete_many({"account_id": user_id})
    return result


async def drop_users(db):
    result = await db.users.drop()
    return result
