from app import schemas


def test_home(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Home": "My blog home project"}


def test_create_user(client):
    response = client.post("/signup/", json={"email": "test1@gmail.com", "password": "password1"})
    new_user = schemas.UserResponse(**response.json())
    assert new_user.email == "test1@gmail.com"
