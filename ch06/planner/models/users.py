from beanie import Document # Benie is a library dedicated to mongodb

from pydantic import BaseModel, EmailStr



class User(Document):
    email: EmailStr
    password: str

    class Settings:
        name = "users"

    class Config:
        json_schema_extra = {
            "example": {
                "email": "fastapi@packt.com",
                "password": "strong!!!",
            }
        }


class UserSignIn(BaseModel):
    email: EmailStr 
    password: str
