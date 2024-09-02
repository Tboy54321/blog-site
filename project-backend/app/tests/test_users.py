from app import schemas

def test_home(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Home": "My blog home project"}

def test_create_user(client):
    response = client.post("/signup/", json={"email": "test1@gmail.com", "password": "password1"})
    new_user = schemas.UserResponse(**response.json())
    assert new_user.email == "test1@gmail.com"

def test_get_users(client):
    response = client.get("/getallusers/")
    assert response.status_code == 200

def test_get_user(authorized_client, test_user):
    response = authorized_client.get(f"/getuser/{test_user['email']}/")
    user = schemas.UserResponse(**response.json())
    assert response.status_code == 200
    assert user.email == test_user['email']

def test_update_profile_info(authorized_client, test_user):
    data = {
        "email": "shit@gmail.com"
    }
    response = authorized_client.put("/update/", json=data)
    new_email = schemas.UserResponse(**response.json())
    assert response.status_code == 200
    assert new_email.email == data['email']

def test_change_password(authorized_client, test_user):
    data = {
        "old_password": "password1",
        "new_password": "password2"
    }
    response = authorized_client.put("/change-password/", json=data)
    assert response.status_code == 200
    assert response.json()['message'] == "Password changed successfully"

def test_change_password_with_wrong_old_password(authorized_client, test_user):
    data = {
        "old_password": "password",
        "new_password": "password2"
    }
    response = authorized_client.put("/change-password/", json=data)
    assert response.status_code == 400
    assert response.json()['detail'] == "Old password does not match"