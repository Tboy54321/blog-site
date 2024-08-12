from fastapi import APIRouter, Depends, status, HTTPException, Response
import models, schemas, oauth2
from sqlalchemy.orm import Session
from database import get_db
import re

router = APIRouter(
    tags=['Comments Endpoint']
)

@router.post("/posts/{id}/comment")
def comment_post(comment: schemas.CommentCreate, id: int, current_user: int = Depends(oauth2.get_current_user), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == current_user.id).first()
    post = db.query(models.BlogPost).filter(models.BlogPost.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")

    new_comment = models.Comment(
        content = comment.content,
        author_id = user.id,
        post_id = id
        )
    db.add(new_comment)
    db.commit()
    return {"Message": "commented successfully"}


@router.delete("/posts/{comment_id}/{id}/delete")
def delete_comment(comment_id: int, id: int, current_user: int = Depends(oauth2.get_current_user), db: Session = Depends(get_db)):
    existing_comment = db.query(models.Comment).filter(models.Comment.post_id == id, models.Comment.id == id).first()
    