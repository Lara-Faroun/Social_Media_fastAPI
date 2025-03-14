from jose import JWTError, jwt
from datetime import datetime, timedelta
from . import schemas , database , models
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from .config import settings

#token url is login endpoint 
outh2_schema = OAuth2PasswordBearer(tokenUrl="login")

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES

def create_access_token(data:dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes= ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp":expire})
    encoded_jwt = jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
    return encoded_jwt

def verify_access_token(token:str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY , algorithms=[ALGORITHM])

        id:str = payload.get("user_id")

        if id is None:
            raise credentials_exception
        
        token_data = schemas.TokenData(id = id)


    except JWTError:
        raise credentials_exception
    
    return token_data

#pass this as a dependency, varify the token and extract the id
#The purpose here is to fetch the user from the DB 
 
def get_current_user(token:str=Depends(outh2_schema),db:Session=Depends(database.get_db)):
    credentials_exception = HTTPException(status_code= status.HTTP_401_UNAUTHORIZED,
                                           detail=f"could not validate credentials", 
                                           headers={"WWW.Authentication":"Bearer"})
    token_data = verify_access_token(token , credentials_exception)
    user = db.query(models.User).filter(models.User.id == token_data.id).first()
    return user 
