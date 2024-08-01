from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base
# , Users, ExpenseCategory, Expense, Budget, UserSettings

DATABASE_URL = "postgresql://postgres:password@localhost:5432/blog_database"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def create_tables():
    Base.metadata.create_all(bind=engine)

def drop_tables():
    Base.metadata.drop_all(bind=engine)

if __name__ == "__main__":
    # drop_tables()
    create_tables()
