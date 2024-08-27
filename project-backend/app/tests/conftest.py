from fastapi.testclient import TestClient
from app.main import app
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
# from config import settings [UVICORN]
from app.config import settings
from app.database import get_db, Base
import pytest
# from alembic import command
import re
from app.oauth2 import create_access_token
from app import models

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


@pytest.fixture
def token(test_user):
    return create_access_token({"user_id": test_user['id']})


@pytest.fixture
def authorized_client(client, token):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }

    return client

@pytest.fixture
def test_posts(session, test_user):
    def generate_slugs(title: str):
        slug = title.lower()
        slug = slug.replace(" ", "-")
        slug = re.sub(r'[^a-z0-9-]', '', slug)
        return slug
    

    post_data = [
        {
            "title": "1st title",
            "content": "1st content",
            "author_id": test_user['id'],
            "slug": "1st-title"
        }, {
            "title": "2nd title",
            "content": "2nd content",
            "author_id": test_user['id'],
            "slug": "2nd-title"
        }, {
            "title": "3rd title",
            "content": "3rd content",
            "author_id": test_user['id'],
            "slug": "3rd-title"
        }, {
            "title": "4th title",
            "content": "4th content",
            "author_id": test_user['id'],
            "slug": "4th-title"
        }
    ]

    def create_post_model(post):
        return models.BlogPost(**post)

    post_map = map(create_post_model, post_data)
    posts = list(post_map)

    session.add_all(posts)
    session.commit()
    posts = session.query(models.BlogPost).all()
    return posts