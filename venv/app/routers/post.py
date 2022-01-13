from typing import Optional, List
from fastapi import FastAPI, Response, exceptions, responses, status, HTTPException, Depends, APIRouter
from .. import models, schema, util, oauth2
from sqlalchemy.orm import Session
from ..database import get_db
from sqlalchemy import func

router = APIRouter(
    prefix = "/posts"
)



@router.get("/")
# def get_posts( db: Session = Depends(get_db), response_model = List[schema.Post],
#     current_user : int = Depends(oauth2.get_current_user ), 
#     limit : int = 10, skip: int = 0, search: Optional[str] = ""):
def get_posts( db: Session = Depends(get_db),
    current_user : int = Depends(oauth2.get_current_user ), response_model = List[schema.PostOut],
    limit : int = 10, skip: int = 0, search: Optional[str] = ""):
    # cursor.execute(""" SELECT * FROM posts """)
    # posts =  cursor.fetchall()
    # return posts
   
    posts =  db.query( models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    result =  db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote,
                 models.Vote.post_id == models.Post.id, isouter = True ).group_by(models.Post.id).all()
    #return posts
    return result

@router.get("/")
def get_current_user_posts( db: Session = Depends(get_db), response_model = List[schema.Post],
    current_user : int = Depends(oauth2.get_current_user ) ):
    # cursor.execute(""" SELECT * FROM posts """)
    # posts =  cursor.fetchall()
    # return posts
    
    posts =  db.query( models.Post).filter(models.Post.owner_id == current_user.id).all()
    #print(posts)
    return posts
    

@router.post("/", status_code= status.HTTP_201_CREATED )
# def create_posts(payload: dict = Body(...)):
def create_posts(post: schema.PostCreate, db: Session = Depends(get_db), response_model = schema.Post,
    current_user : int = Depends(oauth2.get_current_user ) ):
#    cursor.execute(""" INSERT INTO posts(	title, content, published, rating)	VALUES (%s, %s, %s, %s) Returning * """, (post.title, post.content, post.published, post.rating,))
#    conn.commit()	
#    new_post = cursor.fetchone()

   #new_post = models.Post(title= post.title, content =  post.content,  published =  post.published,  rating =  post.rating)
   #**post.dict() does the same thing as title= post.title, content =  post.content,  published =  post.published,  rating =  post.rating for all the colums
   
   # the owner_id is gotten from loggedin user
  
   new_post = models.Post(owner_id=current_user.id, **post.dict())
   db.add(new_post)
   db.commit()
   db.refresh(new_post)
   return new_post


@router.get("/{id}")
def get_post(id:int, db: Session = Depends(get_db), response_model = schema.Post):
    # postValue = find_post(id)
    #
    # print(id)
    # cursor.execute(""" SELECT * FROM posts WHERE ID = %s """, (str(id),))
    # posts =  cursor.fetchone()
    posts = db.query(models.Post).filter(models.Post.owner_id == id).one()
    print(posts)
    if not posts:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                detail= f"post with id: {id} not found")
        #  responses.status_code =  status.HTTP_404_NOT_FOUND
        #  return{'message' : f"post with id: {id} not found"}
    return posts 

  
@router.put("/{id}")
def update_post(id:int, updated_post: schema.PostCreate , db: Session = Depends(get_db),
current_user : int = Depends(oauth2.get_current_user )):
    # cursor.execute(""" UPDATE post set title =%s, content = %s, rating = %S, published = %s WHERE id = %s RETURNING * """, (post.title, post.content, post.rating, post.published, id,))
    # updated_post =  cursor.fetchone()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post == None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                    detail= f"post with id: {id} not found")

    # can't update others post
    if post.owner_id == current_user.id:
        raise HTTPException( status_code= status.HTTP_401_UNAUTHORIZED, 
         detail= f"Not authorize to perform requested action")

    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    db.refresh(post)
       # postValue = find_post(id)
        # if not postValue:
        #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        #             detail= f"post with id: {id} not found")

        # post_dict = post.dict()
        # #index = find_posts_index(id)
        # #my_posts[index] = post_dict
        #  #print(index)
        # my_posts[id-1] = post_dict
       
    return {'mesage':'Updated Successfully', 'data':   post}

# @app.patch("posts/{id}", status_code=HTTP_204_NO_CONTENT)
# def patch_post(id:int):
#  return

@router.delete("/{id}")
def delete_post(id:int,  db: Session = Depends(get_db),
 current_user : int = Depends(oauth2.get_current_user) ):

    # cursor.execute(""" DELETE FROM post where id= %s""", (str(id)),)
    # deleted_post = cursor.fetchone()
    post = db.query(models.Post).filter(models.Post.id == id)
    post_query = post.first()

    if post_query == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                detail= f"post with id: {id} not found")  
    
    # can't delete others post
    if post_query.owner_id == current_user.id:
        raise HTTPException( status_code= status.HTTP_401_UNAUTHORIZED, 
         detail= f"Not authorize to perform requested action")

    post.delete(synchronize_session = False) 
    db.commit
    # postValue = find_post(id)
    # if not postValue:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
    #             detail= f"post with id: {id} not found")        
    # for p in my_posts:
    #      if p['id'] == id:
    #        my_posts.remove(p)
           #return {'message':'post was successfully deleted',  }
        #  for i, p in enumerate( my_posts ):
        #    if p['id'] == id:
        #      my_posts.pop(i)
        #      return {'message':'post was successfully deleted',  }
    return Response(status_code= status.HTTP_204_NO_CONTENT)
