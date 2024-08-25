from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import EmailStr
from sqlalchemy.orm import Session
# import database, models, schemas, utils [UVICRON]
import app.database as database, app.models as models, app.schemas as schemas, app.utils as utils
from sqlalchemy.exc import IntegrityError
# import oauth2 [UVICOON]
import app.oauth2 as oauth2
from typing import List

router = APIRouter(
    # prefix="/user",
    tags=["Signing in new users"]
)

@router.post("/signup/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    hashed_password = utils.get_password_hash(user.password)
    user.password = hashed_password
    new_user = models.User(**user.dict())

    try:
        db.add(new_user)

        db.commit()
        db.refresh(new_user)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists")
    return new_user


# ADMIN ROLE
@router.get("/getallusers", status_code=status.HTTP_200_OK, response_model=List[schemas.UserResponse])
def get_users(db: Session = Depends(database.get_db)):
    all_users = db.query(models.User).all()
    return all_users


@router.get("/getuser/{email}", response_model=schemas.UserResponse)
def get_user(email: EmailStr, db: Session = Depends(database.get_db), current_user: int = Depends(oauth2.get_current_user)):
    user = db.query(models.User).filter(models.User.email == email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User does not exist")
    return user


@router.put("/update", response_model=schemas.UserResponse)
def update_profile_info(updated_user: schemas.UserUpdate, db: Session = Depends(database.get_db), current_user: int = Depends(oauth2.get_current_user)):
    user = db.query(models.User).filter(models.User.email == current_user.email).first()
    print(user)
    print(current_user.id)
    if not updated_user.email:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email is required")
    
    if updated_user.email:
        existing_user = db.query(models.User).filter(models.User.email == updated_user.email).first()
        if existing_user and existing_user.id != current_user.id:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already taken.")
    
    user_query = db.query(models.User).filter(models.User.id == current_user.id)
    user = user_query.first()
    
    if user == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User not found")
    
    update_user = updated_user.dict(exclude_unset=True)
    user_query.update(update_user, synchronize_session=False)

    db.commit()
    
    return user
    

@router.put("/change-password")
def change_password(updated_password: schemas.ChangePassword, db: Session = Depends(database.get_db), current_user: int = Depends(oauth2.get_current_user)):
    user = db.query(models.User).filter(models.User.id == current_user.id).first()

    if not utils.verify_password(updated_password.old_password, user.password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Old password does not match")
    
    hashed_password = utils.get_password_hash(updated_password.new_password)
    user.password = hashed_password

    db.commit()
    db.refresh(user)

    return {"message": "Password changed successfully"}

@router.put("/reset-password")
def reset_password(reset_data = schemas.UserBase, db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.email == reset_data.email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User with this email does not exist.")
    
    token = oauth2.create_access_token(data= {"user_id": user.id})
    # Implemanetation of mail users link


@router.delete("/delete-account")
def delete_password(db: Session = Depends(database.get_db), current_user: int = Depends(oauth2.get_current_user)):
    delete_query = db.query(models.User).filter(models.User.id == current_user.id)
    delete_user = delete_query.first()
    
    db.query(models.BlogPost).filter(models.BlogPost.author_id == delete_user.id).delete(synchronize_session=False)
    db.commit()

    # delete_associations = db.query(models.post_tag_association).filter(models.post_tag_association.c.post_id == id)
    # delete_associations.delete(synchronize_session=False)

    if not delete_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User not found")

    # db.query(models.User).filter(models.BlogPost.author_id == delete_user.id)

    delete_query.delete(synchronize_session=False)
    db.commit()
    
    return {"message": "Account deleted succesfully"}
# Endpoint to handle searching of users