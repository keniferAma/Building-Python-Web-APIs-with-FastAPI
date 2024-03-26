from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from routes.users import user_router
from routes.events import event_router

import uvicorn

app = FastAPI()

# Register routes

app.include_router(user_router,  prefix="/user")
app.include_router(event_router, prefix="/event")


@app.get("/")
async def home():
    return RedirectResponse(url="/event/")
    # If we're placed in the '/' url, we'll be redirect to '/event/'

home.__name__

if __name__ == '__main__':
    uvicorn.run("main:app", host="127.0.1.0", port=8080, reload=True)
    # initializing uvicorn automatically.


#*pip freeze > requirements.txt = para crear un documento dentro del entorno virtual con las 
#librerias instaladas.