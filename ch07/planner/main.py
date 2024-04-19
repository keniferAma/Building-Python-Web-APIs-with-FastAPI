import uvicorn
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from planner.database.connection import Settings
from planner.routes.events import event_router
from planner.routes.users import user_router

settings = Settings()

@asynccontextmanager # here was '.on_event()', currently deprecated.
async def db_startup(app: FastAPI):
    await settings.initialize_database()
    yield

app = FastAPI(lifespan=db_startup)


# register origins

"""Cross-Origin Resource Sharing (CORS) is an HTTP-header based mechanism that allows a server to 
indicate any origins (domain, scheme, or port) other than its own from which a browser should permit 
loading resources.
so, if we send a request from http://myfrontend.com to http://mybackend.com and we don't have set the 
header 'Access-Control-Allow-Origin: *'(which allows any domain to access the resource) 
the client (browser) will refuse to handle the response. (the server response will be blocked by the browser
due to security policies)"""


origins = ["*"] # This is the array with the allowed origins (THE CLIENT, NOT THE SERVER DOMAIN/PORT)
"""
origins = [
“http://packtpub.com”,
“https://packtpub.com”
]
inside we can set the domains allowed, but in our case, we're allowing from anywhere."""


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
