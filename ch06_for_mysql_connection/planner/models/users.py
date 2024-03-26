from sqlalchemy import Boolean, Column, Integer, String, ForeignKey
from database.connection import Base
from pydantic import BaseModel



class User(Base): # this is the model of the table, the equivalent to 'CREATE TABLE Users (user_id INTEGER AUTO_INCREMENT, 
    # username varchar(50) PRIMARY KEY (user_id))'
    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String(50), unique=True)

class Post(Base):
    __tablename__ = 'posts'

    posts_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String(50))
    content = Column(String(100))
    user_id = Column(Integer, ForeignKey(User.user_id, ondelete="cascade", onupdate="restrict"))

class PostBase(BaseModel):
    title: str
    content: str


class UserBase(BaseModel):
    username: str

