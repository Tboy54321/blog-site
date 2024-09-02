from fastapi import APIRouter, Depends, status, HTTPException, Response
# import models, schemas, oauth2 [uvirocn]
import app.models as models, app.schemas as schemas, app.oauth2 as oauth2
from sqlalchemy.orm import Session
# from database import get_db [UVICORN]
from app.database import get_db
from datetime import datetime, timedelta

router = APIRouter(
    tags=['Comments Endpoint']
)

@router.post("/posts/{id}/comment")
def comment_post(comment: schemas.CommentCreate, id: int, current_user: int = Depends(oauth2.get_current_user), db: Session = Depends(get_db)):
    """
    Endpoint to add a comment to a blog post.

    Args:
        comment (schemas.CommentCreate): The content of the comment to be added.
        id (int): The ID of the blog post to which the comment is being added.
        current_user (int): The ID of the current user (automatically fetched from OAuth2 dependency).
        db (Session): The database session (automatically provided by FastAPI dependency injection).

    Returns:
        dict: A success message indicating the comment was added successfully.

    Raises:
        HTTPException: If the blog post with the specified ID does not exist.
    """
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
    """
    Endpoint to retrieve all comments for a specific blog post.

    Args:
        id (int): The ID of the blog post for which comments are being fetched.
        db (Session): The database session (automatically provided by FastAPI dependency injection).
        current_user (int): The ID of the current user (automatically fetched from OAuth2 dependency).

    Returns:
        dict: A list of comments associated with the specified blog post.
    """
    all_comments = db.query(models.Comment).filter(models.Comment.post_id == id).all()
    return {"comments": all_comments}


@router.put("/posts/{id}/comments/{comment_id}")
def update_comment(updated_comment: schemas.CommentCreate, id: int, comment_id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    """
    Endpoint to update a specific comment within a blog post.

    Args:
        updated_comment (schemas.CommentCreate): The new content for the comment.
        id (int): The ID of the blog post containing the comment.
        comment_id (int): The ID of the comment to be updated.
        db (Session): The database session (automatically provided by FastAPI dependency injection).
        current_user (int): The ID of the current user (automatically fetched from OAuth2 dependency).

    Returns:
        schemas.Comment: The updated comment.

    Raises:
        HTTPException: If the comment is not found, or if the time to update the comment has exceeded 10 minutes.
    """
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
    """
    Endpoint to delete a specific comment from a blog post.

    Args:
        comment_id (int): The ID of the comment to be deleted.
        id (int): The ID of the blog post containing the comment.
        current_user (int): The ID of the current user (automatically fetched from OAuth2 dependency).
        db (Session): The database session (automatically provided by FastAPI dependency injection).

    Returns:
        dict: A success message indicating the comment was deleted.

    Raises:
        HTTPException: If the comment does not exist or if the user is not authorized to delete the comment.
    """
    existing_comment = db.query(models.Comment).filter(models.Comment.post_id == id, models.Comment.id == comment_id, models.Comment.author_id == current_user.id).first()
    if not existing_comment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comment does not exist")
    

    db.delete(existing_comment)
    db.commit()
    return {"Message": "Comment deleted successfully"}
    