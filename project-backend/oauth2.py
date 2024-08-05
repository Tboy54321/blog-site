from jose import JWTError, jwt
from datetime import timedelta, datetime
import schemas, database, models
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

SECRET_KEY = "dhsiet95t9ilrddmd,s.cvmnhte[ipd;,d.gtjdlm.gjpd;sde3r-r9r4old,.d,s/.ad/,s.md.t-595[;kndmcbsmfmbueivhdkncsmcdmghru4r74t4r0e-2[pe;q'q\d,mrur8307489peoiwojgkhvnmc.xs,.vmd,.,c.,c,mc.hd08r04rijldg,mcm,bvndcvm]]]"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 300


# CREATING ACCESS TOKEN
def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


#VERIFY THE ACCESS TOKEN
def verify_access_token(token: str, credentials_exception, db: Session):

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
    credentials_exception  = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Could not validate credentials", headers={"WWW-Authenticate": "Berarer"})

    token = verify_access_token(token, credentials_exception, db)
    user = db.query(models.Users).filter(models.Users.id == token.id).first()
    if not user:
        raise credentials_exception
    return user