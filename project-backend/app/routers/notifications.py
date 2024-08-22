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
    notifications = db.query(models.Notification).filter(models.Notification.user_id == current_user.id).order_by(models.Notification.timestamp.desc()).all()
    return notifications