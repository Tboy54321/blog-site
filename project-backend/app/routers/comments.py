from fastapi import APIRouter, Depends, status, HTTPException, Response
import models, schemas, oauth2
from sqlalchemy.orm import Session
from database import get_db
from datetime import datetime, timedelta

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

    if current_user.id == post.author_id:
        pass
    else:
        message = f"{current_user.email} commented on your post your post"

        new_notification = models.Notification(
            user_id=post.author_id,
            post_id=id,
            message=message
        )
        db.add(new_notification)

    db.commit()
    return {"Message": "commented successfully"}


@router.get("/posts/{id}/comments")
def get_comments(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    all_comments = db.query(models.Comment).filter(models.Comment.post_id == id).all()
    return {"comments": all_comments}


@router.put("/posts/{id}/comments/{comment_id}")
def update_comment(updated_comment: schemas.CommentCreate, id: int, comment_id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    comment = db.query(models.Comment).filter(models.Comment.post_id == id, models.Comment.id == comment_id, models.Comment.author_id == current_user.id).first()

    if not comment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found")
    
    if datetime.utcnow() > comment.created_at + timedelta(minutes=10):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="comment time exceeded")
    
    comment.created_at = datetime.utcnow()
    comment.content = updated_comment.content
    db.commit()
    db.refresh(comment)
    return comment


@router.delete("/posts/{comment_id}/{id}/delete")
def delete_comment(comment_id: int, id: int, current_user: int = Depends(oauth2.get_current_user), db: Session = Depends(get_db)):
    existing_comment = db.query(models.Comment).filter(models.Comment.post_id == id, models.Comment.id == comment_id, models.Comment.author_id == current_user.id).first()
    if not existing_comment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comment does not exist")
    

    db.delete(existing_comment)
    db.commit()
    return {"Message": "Comment deleted successfully"}
    