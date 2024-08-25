import pytest
from app import schemas
from .test_database import client, session


@pytest.fixture
def test_user(client):
    user_data = {"email": "test1@gmail.com", "password": "password1"}
    response = client.post("/signup/", json=user_data)
    assert response.status_code == 201
    print(response.json())
    return user_data


def test_home(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Home": "My blog home project"}


# def test_create_user(client, test_user):
#     response = client.post("/signup/", json={"email": test_user['email'], "password": test_user['password']})
#     new_user = schemas.UserResponse(**response.json())
#     assert new_user.email == "test1@gmail.com"


def test_login(client, test_user):
    response = client.post("/login/", data={"username": test_user['email'], "password": test_user['password']})
    assert response.status_code == 200