from typing import Optional, List
from fastapi import FastAPI, Response, exceptions, responses, status, HTTPException, Depends, APIRouter
from .. import models, schema, util, oauth2
from sqlalchemy.orm import Session
from ..database import get_db

router = APIRouter(
    prefix = "/vote",
    tags=['Vote']
)



@router.post("/", status_code=status.HTTP_201_CREATED)
def vote( vote: schema.Vote, db: Session = Depends(get_db), 
    current_user : int = Depends(oauth2.get_current_user ) ) :

    vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id,
        models.Vote.user_id == current_user.id  )
    
    found_vote = vote_query.first()
    post_exist = db.query(models.Post).filter(id == vote.post_id).first()

    if not post_exist:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"post does not exist")
        
    if(vote.dir == 1):
        if found_vote:
            raise HTTPException(status_code= status.HTTP_409_CONFLICT, detail= f"user {current_user.id} has voted on post already {vote.post_id}" )
        new_vote = models.Vote(post_id = vote.post_id, user_id = current_user.id)
        db.add(new_vote)
        db.commit()  

        return{"message": "successfully added vote"}

    else:
        if not found_vote:
            raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail = f"Vote does not exist")
        vote_query.delete
        db.commit()
        return{"message": "successfully deleted vote"}