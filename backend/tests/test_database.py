import os
import pytest

import motor.motor_asyncio
from database import *
from models import User

pytestmark = pytest.mark.asyncio


@pytest.fixture()
def test_db():
    db_name = os.environ.get('DB_NAME', 'MR_TEST')
    db_host = os.environ.get('DB_HOST', 'localhost')
    db_port = os.environ.get('DB_PORT', '27017')
    db_url = "mongodb://" + db_host + ":" + str(db_port) + "/"
    db_client = motor.motor_asyncio.AsyncIOMotorClient(db_url)
    db = db_client[db_name]
    yield db
    db.users.drop()


async def test_insert_user(test_db):
    user_a = User("account1", "pwd1", "a@a")
    result = await insert_user(test_db, user_a)
    assert result and result.acknowledged


async def test_get_user(test_db):
    user_a = User("account1", "pwd1", "a@a")
    result = await find_user(test_db, user_a)
    assert not result
    await insert_user(test_db, user_a)
    result = await find_user(test_db, user_a)
    assert result
