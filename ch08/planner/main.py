import uvicorn
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from planner.database.connection import Settings
from planner.routes.events import event_router
from planner.routes.users import user_router
"""All changes made on the packages were because we named 'ch08' as root, but should've been 'planner'"""

settings = Settings()

@asynccontextmanager # here was '.on_event()', currently deprecated.
async def db_startup(app: FastAPI):
    await settings.initialize_database()
    yield

app = FastAPI(lifespan=db_startup)



# register origins

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routes

app.include_router(user_router, prefix="/user")
app.include_router(event_router, prefix="/event")



@app.get("/")
async def home():
    return RedirectResponse(url="/event/")


if __name__ == '__main__':
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)
