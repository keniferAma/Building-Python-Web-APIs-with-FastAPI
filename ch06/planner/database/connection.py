from typing import Any, List, Optional

from beanie import init_beanie, PydanticObjectId
from models.events import Event
from models.users import User
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic_settings import BaseSettings
from pydantic import BaseModel
"""if you’re writing a script that runs a few queries and doesn’t need to handle many simultaneous 
connections, PyMongo might be simpler and easier to use. But if you’re writing a web server or any 
application that needs to handle many simultaneous connections, AsyncIOMotorClient would be a 
better choice because it allows your application to continue doing other things while waiting 
for the database."""
"""AsyncIOMotorClient is ONLY designed to connect MONGODB"""


class Settings(BaseSettings):
    DATABASE_URL: Optional[str] = None

    async def initialize_database(self):
        client = AsyncIOMotorClient(self.DATABASE_URL)
        await init_beanie(database=client.get_database('blog'), # Here we specify the dabase (If we haven't in the .venv file)
                          document_models=[Event, User]) # These are the collection names.

    class Config: # Reserved class when nested/inherited from BaseSettings, same with 'env_file'
        env_file = ".env"


class Database:
    def __init__(self, model):
        self.model = model

    async def save(self, document) -> None:
        await document.create()
        return

    async def get(self, id: PydanticObjectId) -> Any:
        doc = await self.model.get(id)
        if doc:
            return doc
        return False

    async def get_all(self) -> List[Any]:
        docs = await self.model.find_all().to_list()
        return docs

    async def update(self, id: PydanticObjectId, body: BaseModel) -> Any:
        doc_id = id
        des_body = body.dict()

        des_body = {k: v for k, v in des_body.items() if v is not None}
        update_query = {"$set": {
            field: value for field, value in des_body.items()
        }}

        doc = await self.get(doc_id)
        if not doc:
            return False
        await doc.update(update_query)
        return doc

    async def delete(self, id: PydanticObjectId) -> bool:
        doc = await self.get(id)
        if not doc:
            return False
        await doc.delete()
        return True

settings = Settings() # proving the correct .env functionality.
print(settings.DATABASE_URL)