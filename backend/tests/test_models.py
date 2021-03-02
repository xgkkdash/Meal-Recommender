from models import User


def test_user_info_completed():
    user_a = User("account1", "pwd1", "a@a")
    assert not user_a.info_completed

    user_b = User("account2", "pwd2", "b@b", name="b", age=20, gender="male", height=172, weight=75)
    assert user_b.info_completed
