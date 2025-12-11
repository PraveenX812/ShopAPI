from random import randrange
from typing import Optional, List
from fastapi import FastAPI, HTTPException, Response, status, Depends
from fastapi.params import Body
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from . import models, schema, utils
from sqlalchemy.orm import Session
from .database import engine, SessionLocal

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from . import models
from .database import engine
from .routers import post, user, auth

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

while True:
    try:
        conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres', 
                                password='Praveen!2002', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("DB connected")
        break
    except Exception as error:
        print("DB connection failed")
        print("error", error)
        time.sleep(2)


my_posts = [{"title": "title of post 1", "content": "content of post 1", "id": 1}, {
"title": "favorite foods", "content": "I like pizza", "id": 2}]

def find(id):
    for i in my_posts: 
        if i["id"] == id:
            return i

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)

@app.get("/")
def root():
    return {"message": "Hello World"}
