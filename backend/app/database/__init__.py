import motor.motor_asyncio

from app.config import settings

database = {"client": None}


def get_database():
    return database.get('client')


def connect_db():
    db_client = motor.motor_asyncio.AsyncIOMotorClient(settings.MONGODB_URI)
    database['client'] = db_client[settings.DB_NAME]
