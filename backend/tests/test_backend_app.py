import pytest

from fastapi.testclient import TestClient

from main import app
from models import User


@pytest.fixture
def client():
    client = TestClient(app)
    yield client


@pytest.fixture()
def user():
    return User(account_id='a', password='a', email='a@a')


def test_sign_up(client, user):
    response = client.post("/signup", json=vars(user))
    assert response.status_code == 200


def test_login(client, user):
    pass


def test_auth(client):
    pass
