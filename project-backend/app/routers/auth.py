from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy.orm import Session
# import database, models, utils, oauth2 [UVICORN]
import app.database as database, app.models as models, app.utils as utils, app.oauth2 as oauth2
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from jose import JWTError, jwt
# from oauth2 import SECRET_KEY, ALGORITHM [UVICORN]
from app.oauth2 import SECRET_KEY, ALGORITHM

router = APIRouter(
    tags=['Authentication']
    )

@router.post("/login")
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()

    if not user:
      raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="Invalid Credentials")
    
    if not utils.verify_password(user_credentials.password, user.password):
      raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="Invalid Credentials")
    
    access_token = oauth2.create_access_token(data= {"user_id": user.id})
    refresh_token = oauth2.create_refresh_token(data={"user_id": user.id})
    
    return {"access_token": access_token, 
            "refresh_token": refresh_token,
            "token_type": "bearer"}


@router.post("/logout")
def logout(token: str = Depends(oauth2.oauth2_scheme), db: Session = Depends(database.get_db), current_user: int = Depends(oauth2.get_current_user)):
    blacklisted_token = models.TokenBlacklist(token=token)
    db.add(blacklisted_token)
    db.commit()
    return {"message": "Successfully logged out"}


@router.post("/refresh-token")
def refresh_token(refresh_token: str = Depends(oauth2.oauth2_scheme), db: Session = Depends(database.get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = payload.get("user_id")

        if user_id is None:
            raise credentials_exception

        blacklisted_token = db.query(models.TokenBlacklist).filter(models.TokenBlacklist.token == refresh_token).first()
        if blacklisted_token:
            raise credentials_exception
        
    except JWTError:
        raise credentials_exception
    
    new_access_token = oauth2.create_access_token(data={"user_id": user_id})
    new_refresh_token = oauth2.create_refresh_token(data={"user_id": user_id})
    
    return {
        "access_token": new_access_token,
        "refresh_token": new_refresh_token,
        "token_type": "bearer"
    }
