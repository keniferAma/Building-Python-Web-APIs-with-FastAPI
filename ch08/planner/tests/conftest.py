import asyncio
import httpx
import pytest

from planner.database.connection import Settings
from planner.main import app
from planner.models import User, Event
from planner.auth.jwt_handler import create_access_token


@pytest.fixture(scope='session') # In the context of pytest, a ‘session’ refers to a single run of pytest from start to finish.
# Another perspective: like in asyncio.AsyncClient(), the session doesn't have to repeat every time is needded.
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    """the yield keyword in pytest fixtures is used to pause the fixture function and provide a value 
    to the test function, and then resume the fixture function after the test function finishes to perform 
    any necessary teardown operations."""
    loop.close()
    

async def init_db():
    test_settings = Settings()
    test_settings.DATABASE_URL = "mongodb+srv://admin:comic0413@cluster0.6dgsimp.mongodb.net/"

    await test_settings.initialize_database()


"""So, in these examples, the yield keyword is used to “save” the event loop and HTTP client objects 
and provide them to the test functions. After the test functions finish, the fixtures continue from 
where they left off to perform any necessary cleanup operations."""


@pytest.fixture(scope="session")
async def default_client():             
    await init_db()
    async with httpx.AsyncClient(app=app, base_url="http://localhost:8080/") as client: # Creating a Client session. 
        yield client
        """the yield keyword in pytest fixtures is used to pause the fixture function and provide a value 
        to the test function, and then resume the fixture function after the test function finishes to perform 
        any necessary teardown operations."""

        # Clean up resources 
        """HERE default_client() WAS BEING FINISHING ITS YIELD BECAUSE OF THE CALLING IN THE test_login.py 
        FUNCTIONS, AND THE LOOP WAS BEING TEARDOWN OR FINISHED. THAT'S WHY OF THE RunTimeError by session
        SO, WE HAD TO SWITCH TO scope='function', WHICH LET'S US EXECUTE ALL THE TESTS ONE BY ONE..."""
        
        await Event.find_all().delete()
        await User.find_all().delete()


@pytest.fixture(scope='session')
async def access_token() -> str:
    return create_access_token("testuser@packt.com")


@pytest.fixture(scope="session")
async def mock_event() -> Event:
    new_event = Event(
        creator="testuser@packt.com",
        title="FastAPI Book Launch",
        image="https://linktomyimage.com/image.png",
        description="We will be discussing the contents of the FastAPI book in this event.Ensure to come with your own copy to win gifts!",
        tags=["python", "fastapi", "book", "launch"],
        location="Google Meet"
    )

    await Event.insert_one(new_event)

    yield new_event


"""The client session in your pytest fixture, when defined with scope='session', is created once and lasts 
for the entire test session. This means you can use it in as many test functions as you need 
during that session.

There’s no limit to the number of tests you can do with that session. It will be the same client 
instance for all the tests in that session. This is particularly useful when your tests need to make 
HTTP requests and you want to avoid the overhead of creating a new client for each test."""



# scope by 'function' #
"""Yes, that’s correct. When you set the scope of a pytest fixture to "function", 
it means that a new instance of the fixture is created for each test function. So, 
if you have an event_loop fixture with scope="function", a new event loop is created for each test function.

Here’s how it works:

Before a test function runs, pytest sets up any fixtures that the test function needs. If the fixture is 
function-scoped, a new instance of the fixture is created.
The test function runs, using the instance of the fixture.
After the test function completes, pytest finalizes the fixture (runs any teardown code and discards 
the instance).
So, in the case of your event_loop fixture, a new event loop is opened before each test function runs, 
and then closed after the test function completes. This ensures that each test function gets its 
own event loop, which is open and available for the duration of the test"""

# class #
"""The fixture is set up at the start of the first test method in the class, and torn down after the 
last test method in the class has executed. All test methods in the class share the same instance of 
the fixture. This can be useful if you’re testing different methods of the same class that share common setup."""


# module #
"""The fixture is set up at the start of the first test function in the module, 
and torn down after the last test function in the module has executed. All test functions in 
the module share the same instance of the fixture. This can be useful if you have multiple test 
functions that all require a time-consuming setup, like populating a database with test data"""

# session #
"""The fixture is set up at the start of the test session, and torn down at the end of the test session. 
All test functions in the session share the same instance of the fixture. This can be useful for very 
expensive setup code that should be run as little as possible, but it requires all tests to be able to 
share the same instance of the fixture, which can make tests interfere with each other if not managed carefully."""