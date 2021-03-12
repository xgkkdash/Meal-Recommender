import pytest
from fastapi.security import OAuth2PasswordRequestForm

from fastapi.testclient import TestClient

from app.main import app
from app.database import connect_db, get_database
from app.schemas import User


@pytest.fixture
def client():
    connect_db()
    client = TestClient(app)
    yield client
    get_database().users.drop()


@pytest.fixture()
def user():
    return User(account_id='a', password='a', email='a@a')


def test_sign_up(client, user):
    response = client.post("/signup", json=vars(user))
    assert response.status_code == 200
    assert response.json() == user.dict()


def test_login(client, user):
    test_sign_up(client, user)
    form_data = OAuth2PasswordRequestForm(grant_type="password", username=user.account_id, password=user.password, scope="")
    response = client.post("/login", headers={"Content-Type": "application/x-www-form-urlencoded"}, data=vars(form_data))
    assert response.status_code == 200
    token = response.json().get('access_token')
    assert token
    return token


def test_auth(client, user):
    token = test_login(client, user)
    headers = {"token": token}
    response = client.get("/users/me", headers=headers)
    assert response.status_code == 200
    assert response.json() == user.dict()
