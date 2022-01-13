from fastapi import FastAPI, Response, exceptions, responses, status, HTTPException, Depends, APIRouter
from .. import models, schema, util
from sqlalchemy.orm import Session
from ..database import get_db

router = APIRouter(
    prefix = "/users",
    tags = ['Users']
)

@router.post("/create", response_model = schema.UserOut)
def create_user(user: schema.UserCreate ,  db: Session = Depends(get_db)):
    userExists = db.query(models.User).filter(models.User.email == user.email).first() 

    if userExists: 
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST ,
                detail= f"User with Email: {user.email} already exist")


    #hassh the password
    hashed_password = util.hash(user.password)
    user.password = hashed_password  

    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user



@router.get("/{id}", response_model= schema.UserOut)
def get_user(id:int, db: Session = Depends(get_db), response_model = schema.Post):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                detail= f"User with id: {id} does not exist")
        #  responses.status_code =  status.HTTP_404_NOT_FOUND
        #  return{'message' : f"post with id: {id} not found"}
    return user