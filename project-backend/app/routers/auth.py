from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy.orm import Session
# import database, models, utils, oauth2 [UVICORN]
import app.database as database, app.models as models, app.utils as utils, app.oauth2 as oauth2
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from jose import JWTError, jwt
# from oauth2 import SECRET_KEY, ALGORITHM [UVICORN]
from app.oauth2 import SECRET_KEY, ALGORITHM

# Initialize the APIRouter for authentication routes
router = APIRouter(
    tags=['Authentication']
)

@router.post("/login/", status_code=status.HTTP_200_OK)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    """
    Logs in a user by validating their email and password.
    
    Parameters:
        user_credentials (OAuth2PasswordRequestForm): Contains the 'username' and 'password'.
        db (Session): Database session for querying the user.

    Returns:
        dict: A dictionary containing access_token, refresh_token, and token_type if successful.
    
    Raises:
        HTTPException: If the user is not found or the credentials are invalid.
    """
    # Query the database for a user with the provided email (username)
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()

    # If no user is found, raise an HTTP 406 error
    if not user:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="Invalid Credentials")
    
    # Verify if the provided password matches the stored hashed password
    if not utils.verify_password(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="Invalid Credentials")
    
    # Generate access and refresh tokens for the authenticated user
    access_token = oauth2.create_access_token(data={"user_id": user.id})
    refresh_token = oauth2.create_refresh_token(data={"user_id": user.id})
    
    # Return both tokens and token type
    return {
        "access_token": access_token, 
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }

@router.post("/logout/", status_code=status.HTTP_200_OK)
def logout(token: str = Depends(oauth2.oauth2_scheme), db: Session = Depends(database.get_db), current_user: int = Depends(oauth2.get_current_user)):
    """
    Logs the user out by blacklisting the provided access token.
    
    Parameters:
        token (str): The access token to be blacklisted.
        db (Session): Database session for adding the blacklisted token.
        current_user (int): The currently authenticated user.

    Returns:
        dict: A message confirming the successful logout.
    """
    # Add the current token to the blacklist to prevent its reuse
    blacklisted_token = models.TokenBlacklist(token=token)
    db.add(blacklisted_token)
    db.commit()

    # Return a message indicating successful logout
    return {"message": "Successfully logged out"}


@router.post("/refresh-token")
def refresh_token(refresh_token: str = Depends(oauth2.oauth2_scheme), db: Session = Depends(database.get_db)):
    """
    Refreshes the access and refresh tokens using a valid refresh token.
    
    Parameters:
        refresh_token (str): The refresh token provided by the user.
        db (Session): Database session for checking if the token is blacklisted.

    Returns:
        dict: New access token, refresh token, and token type.
    
    Raises:
        HTTPException: If the token is invalid or blacklisted.
    """
    # Define a standard exception to be raised for invalid credentials
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        # Decode the refresh token to extract the user ID
        payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = payload.get("user_id")

        # If the user_id is not found in the token, raise an exception
        if user_id is None:
            raise credentials_exception

        # Check if the token is blacklisted, if it is, raise an exception
        blacklisted_token = db.query(models.TokenBlacklist).filter(models.TokenBlacklist.token == refresh_token).first()
        if blacklisted_token:
            raise credentials_exception
        
    except JWTError:
        # If there is an error decoding the token, raise an exception
        raise credentials_exception
    
    # Create new access and refresh tokens for the user
    new_access_token = oauth2.create_access_token(data={"user_id": user_id})
    new_refresh_token = oauth2.create_refresh_token(data={"user_id": user_id})
    
    # Return the new tokens and token type
    return {
        "access_token": new_access_token,
        "refresh_token": new_refresh_token,
        "token_type": "bearer"
    }
