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
due to security policies)
* middleware manages all the necessary headers (origin, ...)"""


origins = ["*"] # This is the array with the allowed origins (THE CLIENT, NOT THE SERVER DOMAIN/PORT)
# Here we set the domains allowed
"""
origins = [
“http://packtpub.com”,
“https://packtpub.com”
]
inside we can set the domains allowed, but in our case, we're allowing from anywhere."""


"""
In the context of CORS, a middleware is a type of software that handles the CORS policy for your application. 
It intercepts incoming HTTP requests and adds the necessary CORS headers to the responses before they’re sent 
back to the client1.

Here’s how it works:

When a request comes in, the CORS middleware checks the request’s origin.
-> If the origin is allowed according to the CORS policy set up in the middleware, the middleware adds the 
Access-Control-Allow-Origin header to the response, with the value set to the request’s origin1.

-> The middleware may also add other CORS headers to the response, such as Access-Control-Allow-Methods, 
Access-Control-Allow-Headers, and Access-Control-Allow-Credentials, depending on the CORS policy2.

-> If the request is a preflight request (an OPTIONS request sent by the browser before the actual request, 
to check the server’s CORS policy), the middleware sends a response to the preflight request with the 
appropriate CORS headers1.

-> The actual request is then sent by the browser. If the server’s response to the preflight request indicates 
that the actual request is allowed, the browser processes the response. Otherwise, the browser blocks the 
response.
"""


"""
preflight:

OPTIONS /doc HTTP/1.1
Host: bar.other
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:71.0) Gecko/20100101 Firefox/71.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-us,en;q=0.5
Accept-Encoding: gzip,deflate
Connection: keep-alive
Origin: https://foo.example
Access-Control-Request-Method: POST
Access-Control-Request-Headers: X-PINGOTHER, Content-Type

HTTP/1.1 204 No Content
Date: Mon, 01 Dec 2008 01:15:39 GMT
Server: Apache/2
Access-Control-Allow-Origin: https://foo.example
Access-Control-Allow-Methods: POST, GET, OPTIONS
Access-Control-Allow-Headers: X-PINGOTHER, Content-Type
Access-Control-Max-Age: 86400
Vary: Accept-Encoding, Origin
Keep-Alive: timeout=2, max=100
Connection: Keep-Alive



ONCE THE PREFLIGHT WENT WELL, THE REAL REQUEST OPERATES:

POST /doc HTTP/1.1
Host: bar.other
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:71.0) Gecko/20100101 Firefox/71.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-us,en;q=0.5
Accept-Encoding: gzip,deflate
Connection: keep-alive
X-PINGOTHER: pingpong
Content-Type: text/xml; charset=UTF-8
Referer: https://foo.example/examples/preflightInvocation.html
Content-Length: 55
Origin: https://foo.example   # HERE WE HAVE THE DOMAIN AND PORTS OF OUR PROJECT.
Pragma: no-cache
Cache-Control: no-cache

<person><name>Arun</name></person>

HTTP/1.1 200 OK
Date: Mon, 01 Dec 2008 01:15:40 GMT
Server: Apache/2
Access-Control-Allow-Origin: https://foo.example
Vary: Accept-Encoding, Origin
Content-Encoding: gzip
Content-Length: 235
Keep-Alive: timeout=2, max=99
Connection: Keep-Alive
Content-Type: text/plain"""


app.add_middleware(  
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"], # Either GET, POST, PUT, OPTIONS, DELETE
    allow_headers=["*"], # Either content-type, accept, etc...
)

# Register routes

app.include_router(user_router, prefix="/user")
app.include_router(event_router, prefix="/event")


@app.get("/")
async def home():
    return RedirectResponse(url="/event/")


if __name__ == '__main__':
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)
