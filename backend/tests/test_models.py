from models import User
from schemas import UserBase


def test_user_info_completed():
    user_a = User("account1", "pwd1", "a@a")
    assert not user_a.info_completed

    user_b = User("account2", "pwd2", "b@b", name="b", age=20, gender="male", height=172, weight=75)
    assert user_b.info_completed


def test_from_user_base():
    user_base = UserBase(account_id="account1", password="pwd1", email="a@a")
    user_a = User.from_user_base(user_base)
    assert user_a
