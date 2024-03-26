from fastapi import FastAPI, HTTPException, Depends, status
from pydantic import BaseModel
from typing import Annotated
import models.users
from database.connection import engine, SessionLocal
from sqlalchemy.orm import Session # this is a type hint like List, Dict
import models.users

app = FastAPI()

models.users.Base.metadata.create_all(bind=engine)



def get_db():
    db = SessionLocal()
    try: 
        yield db # Remember, the yield retains the instance until is wasted in the 'create_user' endpoint
    finally: # and this 'finally' will execute once the 'db' is being used.
        db.close()
    # SO WE'RE OPENING THE SESSION, WAIT UNTIL IS USED AND THE finally CLOSES IT.
    # CLOSSING THE SESSION DOESN'T MEAN WE'RE CLOSING THE DATABASE CONNECTION.

db_dependency = Annotated[Session, Depends(get_db)]
# Here we're adding metadata with a first value as 'Session' which is a type hint, telling
# to 'db_dependecy' MUST be a Session
"""“In the create_user function, db: db_dependency is telling FastAPI 
“I need a Session instance for this request, and you can get one by calling get_db”.”"""


@app.post('/users', status_code=status.HTTP_201_CREATED)
async def create_user(user: models.users.UserBase, db: db_dependency):
    db_user = models.users.User(**user.model_dump())
    db.add(db_user)
    db.commit()

@app.get('/users/all', status_code=status.HTTP_200_OK)
async def get_all_users(db: db_dependency):
    users = db.query(models.users.User).all()
    if users is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Table is empty')
    return users
    # or just '{"users": [ user for user in users]}' will retrieve the list with 

@app.post('/posts', status_code=status.HTTP_201_CREATED)
async def create_posts(user: models.users.PostBase, db: db_dependency):
    db_post = models.users.Post(**user.model_dump())
    db.add(db_post)
    db.commit()

"""Depends() gives the result (on this case to 'db')(by calling a function), while a regular 
type hint provides a ‘model’ or expectation of what type the parameter should be. """


@app.get('/users/{user_id}', status_code=status.HTTP_200_OK)
async def get_user_id(user_id: int, db: db_dependency):
    user = db.query(models.users.User).filter(models.users.User.user_id == user_id).first() # Calling the TABLE not the BaseModel class
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='The user was not found.')
    return user # If we want to retrieve an specific row: {"username": user.username} 
    


@app.delete('/user/delete/{user_id}', status_code=status.HTTP_202_ACCEPTED)
async def delete_user(user_id: int, db: db_dependency):
    user = db.query(models.users.User).filter(models.users.User.user_id == user_id).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='The user was not found.')
    db.delete(user)
    db.commit()    


