from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base
from config import settings

# DATABASE_URL = "postgresql://postgres:password@localhost:5432/blog_database"
DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def create_tables():
    Base.metadata.create_all(bind=engine)

def drop_tables():
    Base.metadata.drop_all(bind=engine)

if __name__ == "__main__":
    drop_tables()
    # create_tables()