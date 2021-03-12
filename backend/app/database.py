import motor.motor_asyncio

from app.config import settings
from app.schemas import User


async def insert_user(db, user: User):
    doc = await db.users.insert_one(user.dict())
    return doc


async def find_user(db, user_id):
    doc = await db.users.find_one({"account_id": user_id})
    if doc:
        doc.pop("_id", None)
    return User(**doc) if doc else None


async def drop_users(db):
    result = await db.users.drop()
    return result

database = {"client": None}


def get_database():
    return database.get('client')


def connect_db():
    db_client = motor.motor_asyncio.AsyncIOMotorClient(settings.MONGODB_URI)
    database['client'] = db_client[settings.DB_NAME]


# db_client = motor.motor_asyncio.AsyncIOMotorClient(settings.MONGODB_URI)
# database = db_client[settings.DB_NAME]
