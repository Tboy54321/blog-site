from fastapi.testclient import TestClient
from app.main import app
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
# from config import settings [UVICORN]
from app.config import settings
from app.database import get_db, Base
import pytest
# from alembic import command

SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base.metadata.create_all(bind=engine)

# def override_get_db():
#     try:
#         db = TestingSessionLocal()
#         yield db
#     finally:
#         db.close()

# app.dependency_overrides[get_db] = override_get_db


@pytest.fixture()
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


# client = TestClient(app)
@pytest.fixture()
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


@pytest.fixture
def test_user(client):
    user_data = {"email": "test2@gmail.com", "password": "password1"}
    response = client.post("/signup/", json=user_data)
    # assert response.status_code == 201
    new_user = response.json()
    new_user['password'] = user_data['password']
    return new_user
