from fastapi import APIRouter, Depends, status, HTTPException, Response
# import models, schemas, oauth2 [UVICORN]
import app.models as models, app.schemas as schemas, app.oauth2 as oauth2
from sqlalchemy.orm import Session
# from database import get_db [UVIRCORN]
from app.database import get_db

router = APIRouter(
    tags=["Notificaions Endpoint"]
)

@router.get("/notifications")
def get_notifications(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    """
    Endpoint to retrieve all notifications for the current user.

    Args:
        db (Session): The database session (automatically provided by FastAPI dependency injection).
        current_user (int): The ID of the current user (automatically fetched from OAuth2 dependency).

    Returns:
        List[schemas.NotificationResponse]: A list of notifications for the current user, ordered by timestamp in descending order.

    """
    notifications = db.query(models.Notification).filter(models.Notification.user_id == current_user.id).order_by(models.Notification.timestamp.desc()).all()
    return notifications