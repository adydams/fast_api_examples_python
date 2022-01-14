from jose import JWTError, jwt
from datetime import datetime, timedelta

from secrets import token_bytes
from base64 import b64encode
from . import schema, database, models

from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
oauth2_scheme = OAuth2PasswordBearer(tokenUrl= 'login')

from sqlalchemy.orm import Session
from decouple import config


SECRET_KEY_Val = config('SECRET_KEY')
ALGORITHM_Val = config('ALGORITHM')
ACCESS_TOKEN_EXPIRE_MINUTES_Val = int(config('ACCESS_TOKEN_EXPIRE_MINUTES'))
# SECRET_KEY
# algorithm
# expiration_time


SECRET_KEY = SECRET_KEY_Val
ALGORITHM = ALGORITHM_Val
ACCESS_TOKEN_EXPIRE_MINUTES = ACCESS_TOKEN_EXPIRE_MINUTES_Val

def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp" : expire})
    
    #data to encode, secret, algorithm
    encode_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm = ALGORITHM)
    
    return encode_jwt

def verify_access_token(token: str, credential_exception):
    try: 
          
        payload = jwt.decode(token, SECRET_KEY, algorithms= ALGORITHM) 
        
        id: str = payload.get("user_id")
        email: str = payload.get("user_email")

        if id is None:
            raise credential_exception

        token_data = schema.TokenData(id = id, email = email )
    except JWTError:
        raise credential_exception

    return token_data

def get_current_user(token: str = Depends(oauth2_scheme),  db: Session = Depends(database.get_db)):
    credentials_exception = HTTPException( status_code= status.HTTP_401_UNAUTHORIZED, detail = f"Could not validate credentials",
    headers ={"WWW-Authenticate": " Bearer"})

    token = verify_access_token(token, credentials_exception )
    
    user = db.query(models.User).filter(models.User.id == token.id).first()
    
    return user
      
