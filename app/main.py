from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from typing import Optional, List
from fastapi.params import Body
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time

from sqlalchemy.sql.expression import false
from . import models, schema, util
from .database import engine, get_db
from sqlalchemy.orm import Session

# not necessary any more since we now use alembic to generate, migrate tables
#models.Base.metadata.create_all(bind=engine)

from starlette.responses import Response
from starlette.status import HTTP_204_NO_CONTENT

from .routers import post, user, auth, vote

app = FastAPI()


# while True:

#     try:
#         conn = psycopg2.connect(host='localhost', database ='fastapi', user='postgres', password ='@Beautiful1989',
#         cursor_factory=RealDictCursor)
#         cursor = conn.cursor()
#         print("Database connection was successful!")
#         break   
#     except Exception as error:
#         print("Connecting to database failed!")
#         print("Error:", error) 
#         time.sleep(2)
origins  = ["*"] #["https://www.google.com"] 

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

my_posts =[{"id": 1," title": "Last read book", "content": "Master piece"},
 {"id": 2," title": "Favorite food", "content": "Plantain"},
 {"id": 3," title": "Last personal development", "content": "learnt making cartoon with adobe animator"}
]

def find_post(id):
    for p in my_posts:
        if p['id'] == id:
            return p

def find_posts_index(id:int):
    for i, p in enumerate( my_posts):
        return i

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)


@app.get("/")
def root():
    return {"data": my_posts}


    