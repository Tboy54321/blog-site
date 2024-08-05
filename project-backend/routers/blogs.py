from fastapi import FastAPI, APIRouter, Depends
import models, schemas, oauth2
from sqlalchemy.orm import Session
from database import get_db

router = APIRouter(tags=["Blogs Page"])
# app = FastAPI()


@router.get("/posts")
def get_all_blogs(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    all_blogs = db.query(models.blogs).all()
    return all_blogs


@router.get("/posts/:{id}")
def get_one_post(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    blog = db.query(models.blogs.id == id).first()
    return blog