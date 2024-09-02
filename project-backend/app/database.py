from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
# from config import settings [UVICORN]
from app.config import settings

# Database URL construction
# SQLALCHEMY_DATABASE_URL = "postgresql://postgres:password@localhost:5432/blog_database"
SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"

# Create the SQLAlchemy engine
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Create a configured "Session" class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for declarative models
Base = declarative_base()

def get_db():
    """
    Dependency for getting a database session.

    This function provides a database session to be used in API endpoints.
    It ensures that the session is properly closed after use.

    Yields:
        Session: An SQLAlchemy session instance.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()