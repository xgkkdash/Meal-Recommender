import pytest
from fastapi.security import OAuth2PasswordRequestForm

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
    form_data = OAuth2PasswordRequestForm(grant_type="password", username=user.account_id, password=user.password, scope="")
    response = client.post("/login", headers={"Content-Type": "application/x-www-form-urlencoded"}, data=vars(form_data))
    assert response.status_code == 200
    token = response.json().get('access_token')
    assert token
    return token


def test_auth(client, user):
    token = test_login(client, user)
    headers = {"Authorization": token}
    response = client.get("/users/me", headers=headers)
    assert response.status_code == 200
    assert response.json()
