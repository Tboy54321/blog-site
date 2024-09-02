from jose import JWTError, jwt
from datetime import timedelta, datetime
# import schemas, database, models [UVICORN]
import app.schemas as schemas, app.database as database, app.models as models
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
# from config import settings [UVICORN]
from app.config import settings


# OAuth2 scheme for handling token-based authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

# Configuration for JWT encoding and decoding
SECRET_KEY = f"{settings.secret_key}"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes
REFRESH_TOKEN_EXPIRE_DAYS = settings.refresh_token_expire_days


# CREATING ACCESS TOKEN
def create_access_token(data: dict):
    """
    Create an access token for authentication.

    Args:
        data (dict): The data to include in the token's payload.

    Returns:
        str: The encoded JWT access token.
    """
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


# REFRESH ACCESS TOKEN
def create_refresh_token(data: dict):
    """
    Create a refresh token for extending session validity.

    Args:
        data (dict): The data to include in the token's payload.

    Returns:
        str: The encoded JWT refresh token.
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


#VERIFY THE ACCESS TOKEN
def verify_access_token(token: str, credentials_exception, db: Session):
    """
    Verify the validity of an access token.

    Args:
        token (str): The token to verify.
        credentials_exception (HTTPException): Exception to raise if verification fails.
        db (Session): Database session for checking blacklisted tokens.

    Returns:
        schemas.TokenData: Token data if the token is valid.
    """
    try:

        # blacklisted_token = db.query(models.TokenBlacklist).filter(models.TokenBlacklist.token).first()
        blacklisted_token = db.query(models.TokenBlacklist).filter(models.TokenBlacklist.token == token).first()

        if blacklisted_token:
            raise credentials_exception
        
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        # print(payload)

        id: int = payload.get("user_id")

        if id is None:
            raise credentials_exception
        
        token_data = schemas.TokenData(id=id)

    except JWTError as J:
        raise credentials_exception
    
    return token_data
    

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    """
    Retrieve the current user based on the provided token.

    Args:
        token (str): The authentication token.
        db (Session): Database session for querying user information.

    Returns:
        models.User: The user corresponding to the token.

    Raises:
        HTTPException: If the token is invalid or user does not exist.
    """
    credentials_exception  = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Could not validate credentials", headers={"WWW-Authenticate": "Berarer"})

    token = verify_access_token(token, credentials_exception, db)
    user = db.query(models.User).filter(models.User.id == token.id).first()
    if not user:
        raise credentials_exception
    return user
