from fastapi import APIRouter, Depends, status, HTTPException, Response
# import models, schemas, oauth2 [UVICORN]
import app.models as models, app.schemas as schemas, app.oauth2 as oauth2
from sqlalchemy.orm import Session
# from database import get_db [UVICRON]
from app.database import get_db
import re

router = APIRouter(
    tags=['Like Endpoint']
)

@router.post("/posts/{id}/like")
def like_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    post = db.query(models.BlogPost).filter(models.BlogPost.id == id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    
    like_query = db.query(models.Like).filter(models.Like.post_id == id, models.Like.user_id == current_user.id)
    found_like = like_query.first()

    if found_like:
        raise HTTPException(status_code=status.HTTP_429_TOO_MANY_REQUESTS, detail="Post already liked")
    
    new_like = models.Like(user_id = current_user.id, post_id = id)
    db.add(new_like)

    if current_user.id == post.author_id:
        pass
    else:
        message = f"{current_user.email} liked your post"

        new_notification = models.Notification(
            user_id=post.author_id,
            post_id=id,
            message=message
        )
        db.add(new_notification)

    # print(message)
    db.commit()
    # db.refresh(new_like)
    return {"Message": "Post liked"}


@router.delete("/posts/{id}/unlike")
def unlike_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    post = db.query(models.BlogPost).filter(models.BlogPost.id == id).first()
    
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not exist")
    
    unlike_query = db.query(models.Like).filter(models.Like.post_id == id, models.Like.user_id == current_user.id)
    found_unlike = unlike_query.first()

    if not found_unlike:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Like not found")
    
    unlike_query.delete(synchronize_session=False)
    db.commit()
    return {"message": "Post unliked"}

