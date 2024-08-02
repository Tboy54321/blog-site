from fastapi import FastAPI, APIRouter, Depends
import models, schemas
from sqlalchemy.orm import Session
from database import get_db

router = APIRouter()
# app = FastAPI()

@router.get("/blogs")
def get_all_blogs(db: Session = Depends(get_db)):
  all_blogs = db.query(models.blogs).all()
  print(all_blogs)
  return{"all blogs": "a sample"}