from fastapi import FastAPI, APIRouter, Depends, HTTPException, status
import models, schemas, oauth2
from sqlalchemy.orm import Session
from database import get_db

router = APIRouter(tags=["Blogs Page"])
# app = FastAPI()


@router.get("/posts")
def get_all_blogs(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    all_blogs = db.query(models.BlogPost).all()
    print(current_user)
    return all_blogs


@router.get("/posts/{id}")
def get_one_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    blog = db.query(models.BlogPost).filter(models.BlogPost.id == id).first()
    
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id {id} does not exist")
    
    return blog


# @router.post("/post"):
# def new_post(post: schemas, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
#     blog = db.query
#     db.add