import os
import pytest
from pymongo.errors import DuplicateKeyError

import motor.motor_asyncio
from database import *
from models import User

pytestmark = pytest.mark.asyncio


@pytest.fixture()
def test_db():
    db_name = os.environ.get('DB_NAME', 'MR_DEV')
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
    assert result.inserted_id == user_a.account_id
    user_aa = User("account1", "pwd11", "a@aa")
    with pytest.raises(DuplicateKeyError):
        await insert_user(test_db, user_aa)


async def test_get_user(test_db):
    user_a = User("account1", "pwd1", "a@a")
    result = await find_user(test_db, user_a)
    assert not result
    await insert_user(test_db, user_a)
    result = await find_user(test_db, user_a)
    assert result
