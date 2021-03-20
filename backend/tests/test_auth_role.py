import pytest
from fastapi.security import OAuth2PasswordRequestForm

from fastapi.testclient import TestClient

from app.main import app
from app.database import connect_db
from app.schemas import User


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


def login_to_get_token(cli, user, is_admin=False):
    url = "/login/admin" if is_admin else "/login"
    form_data = OAuth2PasswordRequestForm(grant_type="password", username=user.account_id, password=user.password,
                                          scope="")

    response = cli.post(url, headers={"Content-Type": "application/x-www-form-urlencoded"}, data=vars(form_data))
    token = response.json().get('access_token')
    return token


def test_regular_user_get_all_users(client, regular_user):
    token = login_to_get_token(client, regular_user)
    headers = {"token": token}
    response = client.get("/users", headers=headers)
    assert response.status_code == 403  # Permission not enough, Forbidden


def test_admin_user_get_all_users(client, admin_user):
    token = login_to_get_token(client, admin_user, is_admin=True)
    headers = {"token": token}
    response = client.get("/users", headers=headers)
    assert response.status_code == 200
    for user in response.json():
        assert isinstance(user, User)
