from app import schemas
import pytest
from jose import jwt
from app.config import settings


def test_root(client):
    res = client.get("/")
    assert res.json().get("message") == "Hello World"
    assert res.status_code ==200

def test_create_user(client):
    res = client.post("/users/" ,
     json = {
        "name": "Test user",
        "email": "testuser@example.com",
        "password": "password123"
    })
    new_user = schemas.UserResponse(**res.json())
    assert new_user.email == "testuser@example.com"
    assert res.status_code == 201 

def test_login_user(client,test_user):    
    res = client.post("/login" ,
     data = {
        "username": test_user['email'],
        "password": test_user['password']
    })
    login_res = schemas.Token(**res.json())
    #To validate login_res we need to decode the accesstoken and check the id
    payload = jwt.decode(login_res.access_token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    assert payload.get("user_id") == test_user['id']
    assert login_res.token_type == "bearer"
    assert res.status_code == 200



@pytest.mark.parametrize("email, password, status_code",[
    ('wrongemail@gmail.com', 'password123', 403),
    ('testuser@example.com', 'wrongpassword', 403),
    ('wrongemail@gmail.com', 'wrongpassword', 403),
    (None, 'password123', 403),
    ('testuser@example.com', None, 403)
])
def test_incorrect_login(client,test_user,email, password, status_code):    
    res = client.post("/login" ,
     data = {
        "username": email,
        "password": password
    })
    assert res.status_code == status_code

