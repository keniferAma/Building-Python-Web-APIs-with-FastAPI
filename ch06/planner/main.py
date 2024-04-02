import uvicorn
from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from database.connection import Settings
from routes.events import event_router
from routes.users import user_router
from contextlib import asynccontextmanager



settings = Settings()

@asynccontextmanager # To startup 
async def init_db(app: FastAPI): 
    await settings.initialize_database() # code to run on startup 
    yield # Code to run on shutdown (it is NECESSARY for the @contextmanager but could be empty)


app = FastAPI(lifespan=init_db) # lifespan: duracion, vida util. se ejecuta al iniciar la aplicacion



# Register routes

app.include_router(user_router, prefix="/user")
app.include_router(event_router, prefix="/event")




@app.get("/")
async def home():
    return RedirectResponse(url="/event/")


if __name__ == '__main__':
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)

