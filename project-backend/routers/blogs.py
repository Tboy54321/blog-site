from fastapi import FastAPI, APIRouter, Depends
import models, schemas
from sqlalchemy.orm import Session
from database import get_db

router = APIRouter(tags=["Blogs Page"])
# app = FastAPI()

@router.get("/blogs")
def get_all_blogs(db: Session = Depends(get_db)):
    all_blogs = db.query(models.blogs).all()
    return all_blogs