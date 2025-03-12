from app.main import app
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import settings
from app.database import get_db, Base
import pytest
from fastapi.testclient import TestClient

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

