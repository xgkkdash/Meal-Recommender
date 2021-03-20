from app.schemas import UserRole


async def insert_user_role(db, user_role: UserRole):
    doc = await db.user_roles.insert_one(user_role.dict())
    return doc


async def find_user_role(db, user_role: UserRole):
    doc = await db.user_roles.find_one(user_role.dict())
    if doc:
        doc.pop("_id", None)
    return UserRole(**doc) if doc else None


async def find_roles_of_user(db, user_id: str):
    docs = [doc async for doc in db.user_roles.find({"user_id": user_id})]
    for doc in docs:
        doc.pop("_id", None)
    user_roles = [UserRole(**doc) for doc in docs]
    return user_roles


async def update_user_role(db, user_role: UserRole):
    old_doc = await db.user_roles.find_one({"user_id": user_role.user_id})
    result = await db.user_roles.replace_one({'_id': old_doc['_id']}, user_role.dict())
    return result


async def delete_user_role(db, user_role: UserRole):
    result = await db.user_roles.delete_many(user_role.dict())
    return result


async def drop_user_roles(db):
    result = await db.user_roles.drop()
    return result
