from app import schemas
from .test_database import client, session

def test_login(client):
    response = client.post("/login/", data={"username": "test1@gmail.com", "password": "password1"})
    assert response.status_code == 200