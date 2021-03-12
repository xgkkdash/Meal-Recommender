import pytest

import motor.motor_asyncio
from app.config import settings
from app.database import insert_user, find_user, drop_users
from app.schemas import User

pytestmark = pytest.mark.asyncio


@pytest.fixture()
def test_db():
    client = motor.motor_asyncio.AsyncIOMotorClient(settings.MONGODB_URI)
    db = client[settings.DB_NAME]
    yield db
    db.users.drop()


@pytest.fixture()
def user():
    return User(account_id="account1", password="pwd1", email="a@a")


async def test_insert_and_find_user(test_db, user):

    result = await find_user(test_db, user.account_id)
    assert not result

    result = await insert_user(test_db, user)
    assert result and result.acknowledged

    result = await find_user(test_db, user.account_id)
    assert result
    assert result == user


async def test_drop_users(test_db, user):
    result = await insert_user(test_db, user)
    assert result and result.acknowledged

    await drop_users(test_db)
    result = await find_user(test_db, user.account_id)
    assert not result
