from typing import Optional, List
from fastapi import FastAPI, Response, exceptions, responses, status, HTTPException, Depends, APIRouter
from fastapi.security.oauth2 import  OAuth2PasswordRequestForm
from .. import models, schema, util, oauth2
from sqlalchemy.orm import Session
from .. import database


router = APIRouter(
    tags = ['authentication']
)


@router.post("/login", response_model= schema.Token)
def login( user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):

    # OAuth2PasswordRequestForm is a data object serialized into username and password
    userExists = db.query(models.User).filter(models.User.email == user_credentials.username).first()
    #valueOnVerify =  util.verify_password( user_credentials.password, userExists.password )
    #print("verify password result")
    #print(valueOnVerify)

    if not userExists :
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN ,
                detail= f"Invalid credentials")

    if not util.verify_password( user_credentials.password, userExists.password ):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN ,
                detail= f"Invalid credentials")

    #passing user credential into dict form
    access_token = oauth2.create_access_token(data = {"user_id":userExists.id, "user_email": userExists.email })
    return{"access_token": access_token, "token_type": "bearer"}

    