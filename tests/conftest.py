#This a a file that contains all the fixtures that are used in the test cases
#This is a special file that pytest usses, it will allow us to define fixtures
#  that can be used across multiple test files.

from app.main import app
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import settings
from app.database import get_db, Base
import pytest
from fastapi.testclient import TestClient
from app.oauth2 import create_access_token
from app import models

SQLALCHEMY_DATABASE_URL = settings.SQLALCHEMY_TEST_DATABASE_URL

print(SQLALCHEMY_DATABASE_URL)

# The engine is responsible for establishing the connection  
engine = create_engine(SQLALCHEMY_DATABASE_URL)

#We need a a session to talk to the SQL DB
TestingSessionlocal = sessionmaker(autocommit=False, autoflush=False,bind=engine)




#The benefet of the the session fixture and client fixture this way, is that you can access to session 

@pytest.fixture
def session():
    Base.metadata.drop_all(bind = engine)
    Base.metadata.create_all(bind = engine)
    db = TestingSessionlocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db] = override_get_db

    yield TestClient(app)

@pytest.fixture
def test_user(client):
    user_data = {
        "name": "Test user",
        "email": "testuser@example.com",
        "password": "password123"
    }

    res = client.post("/users/" , json = user_data)
    new_user = res.json()
    new_user['password'] = user_data['password']
    return new_user


@pytest.fixture
def test_user2(client):
    user_data = {
        "name": "Test user2",
        "email": "testuser2@example.com",
        "password": "password123"
    }

    res = client.post("/users/" , json = user_data)
    new_user = res.json()
    new_user['password'] = user_data['password']
    return new_user

@pytest.fixture
def token(test_user):
    return create_access_token(data={"user_id": test_user['id']})

@pytest.fixture
def authorized_client(client , token):  
    #adding the Authorization header to the client
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"  
    }
    return client

@pytest.fixture
def test_posts(test_user , session,test_user2):
    post_data = [
        {"title": "title1", "content":"content1" , "owner_id" :test_user['id']},
        {"title": "title2", "content":"content2" , "owner_id" :test_user['id']},
        {"title": "title3", "content":"content3" , "owner_id" :test_user['id']},
        {"title": "title4", "content":"content4" , "owner_id" :test_user2['id']}

    ]

    def create_post_model(post):
        return models.Post(**post)
    
    post_map = map(create_post_model, post_data)
    posts = list(post_map)

    session.add_all(posts)
    session.commit()

    posts = session.query(models.Post).all()
    return posts

@pytest.fixture()
def test_vote(test_user , test_posts , session):
    new_vote = models.Vote(post_id=test_posts[3].id, user_id=test_user['id'])
    session.add(new_vote)
    session.commit()
