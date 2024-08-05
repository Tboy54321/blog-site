from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy.orm import Session
import database, models, utils, oauth2
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

router = APIRouter(tags=['Authentication'])

@router.post("/login")
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    user = db.query(models.Users).filter(models.Users.email == user_credentials.username).first()

    if not user:
      raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="Invalid Credentials")
    
    if not utils.verify_password(user_credentials.password, user.password):
      raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="Invalid Credentials")
    
    access_token = oauth2.create_access_token(data= {"user_id": user.id})
    
    return {"access_token": access_token, "token_type": "bearer"}
    
