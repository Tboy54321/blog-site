import pytest
from app import schemas
from jose import jwt
from app.config import settings


SECRET_KEY = f"{settings.secret_key}"
ALGORITHM = settings.algorithm

def test_login(client, test_user):
    response = client.post("/login/", data={"username": test_user['email'], "password": test_user['password']})
    login_res = schemas.Token(**response.json())
    payload = jwt.decode(login_res.access_token, SECRET_KEY, algorithms=[ALGORITHM])
    id = payload.get("user_id")
    assert id == test_user['id']
    assert login_res.token_type == "bearer"
    assert response.status_code == 200


@pytest.mark.parametrize("email, password, status_code", [
    ("wrongemail@gmail.com", "password", 406),
    ("test@gmail.com", "wrongpassword", 406),
    ("wrongemail@gmail.com", "wrongpassword", 406),
    (None, "password", 422)
])
def test_failed_login(client, test_user, email, password, status_code):
    response = client.post("/login/", data={"username": email, "password": password})
    
    assert response.status_code == status_code
    # assert response.json().get('detail') == "Invalid Credentials"

def test_logout