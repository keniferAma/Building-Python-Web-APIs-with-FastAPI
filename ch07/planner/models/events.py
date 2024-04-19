from typing import Optional, List

from beanie import Document
from pydantic import BaseModel, Field


class Event(Document):
    creator: Optional[str] = Field(None)
    title: str
    image: str
    description: str
    tags: List[str]
    location: str

    class Config: #Config belongs to pydantic, while Settings class to Beanie
        json_schema_extra = {
            "example": {
                "title": "FastAPI BookLaunch",
                "image": "https://linktomyimage.com/image.png",
                "description": "We will be discussing the contents of the FastAPI book in this event.Ensure to come with your own copy to win gifts!",
                "tags": ["python", "fastapi", "book", "launch"],
                "location": "Google Meet"
            }
        }

    class Settings: #Specifying the collection names through the Settings by Beanie
        name = "events" 


class EventUpdate(BaseModel):
    title: Optional[str] = Field(None)
    image: Optional[str] = Field(None)
    description: Optional[str] = Field(None)
    tags: Optional[List[str]] = Field(None)
    location: Optional[str] = Field(None)

    class Config:
        json_schema_extra = {
            "example": {
                "title": "FastAPI BookLaunch",
                "image": "https://linktomyimage.com/image.png",
                "description": "We will be discussing the contents of the FastAPI book in this event.Ensure to come with your own copy to win gifts!",
                "tags": ["python", "fastapi", "book", "launch"],
                "location": "Google Meet"
            }
        }
