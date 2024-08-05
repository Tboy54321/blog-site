from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import EmailStr
from sqlalchemy.orm import Session
import database, models, schemas, utils
from sqlalchemy.exc import IntegrityError

router = APIRouter(
    # prefix="/user",
    tags=["Signing in new users"]
)

@router.post("/signin", status_code=status.HTTP_201_CREATED)
def create_user(user: schemas.UserBase, db: Session = Depends(database.get_db)):
    hashed_password = utils.get_password_hash(user.password)
    user.password = hashed_password
    new_user = models.Users(**user.dict())

    try:
        db.add(new_user)

        db.commit()
        db.refresh(new_user)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists")
    return new_user

@router.get("/getallusers", status_code=status.HTTP_200_OK)
def get_users(db: Session = Depends(database.get_db)):
    all_users = db.query(models.Users).all()
    return all_users

@router.get("/getuser/{email}")
def get_user(email: EmailStr, db: Session = Depends(database.get_db)):
    user = db.query(models.Users).filter(models.Users.email == email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User does not exist")
    return {"Mail Exist": user}