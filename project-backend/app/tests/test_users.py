from fastapi.testclient import TestClient
from app.main import app
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
# from config import settings [UVICORN]
from app.config import settings
from app.database import get_db, Base
from app import schemas
import pytest
from alembic import command


SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db


@pytest.fixture
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


# client = TestClient(app)
@pytest.fixture
def client(session):
    # command.downgrade("base")
    # command.upgrade("head")
    def override_get_db():
        try:
            yield session
        finally:
            session.close()
            app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)


def test_home(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Home": "My blog home project"}


def test_create_user(client):
    response = client.post("/signup", json={"email": "test1@gmail.com", "password": "password1"})
    new_user = schemas.UserResponse(**response.json())
    assert new_user.email == "test1@gmail.com"


# def test_get_users(client):
#     response = client.get("/getallusers")
#     users = schemas.UserResponse(**response.json())
    