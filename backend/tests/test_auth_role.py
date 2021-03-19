import pytest

from fastapi.testclient import TestClient

from app.main import app
from app.database import connect_db
from app.schemas import User
from app.utils import generate_token


@pytest.fixture
def client():
    connect_db()
    client = TestClient(app)
    yield client


@pytest.fixture()
def regular_user():
    return User(account_id='a', password='a', email='a@a')


@pytest.fixture()
def admin_user():
    return User(account_id='admin', password='admin', email='admin@admin')


def test_regular_user_get_all_users(client, regular_user):
    token = generate_token(regular_user.account_id)
    headers = {"token": token}
    response = client.get("/users", headers=headers)
    assert response.status_code == 403  # Permission not enough, Forbidden


def test_admin_user_get_all_users(client, admin_user):
    token = generate_token(admin_user.account_id)
    headers = {"token": token}
    response = client.get("/users", headers=headers)
    assert response.status_code == 200
    for user in response.json():
        assert isinstance(user, User)
