from dataclasses import asdict

from models import User


async def insert_user(db, user: User):
    doc = await db.users.insert_one(asdict(user))
    return doc


async def find_user(db, user: User):
    doc = await db.users.find_one({"account_id": user.account_id})
    if doc:
        doc.pop("_id", None)
    return User(**doc) if doc else None


async def drop_users(db):
    result = await db.users.drop()
    return result
