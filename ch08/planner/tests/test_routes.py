import httpx
import pytest

from planner.models import Event


# @pytest.mark.order(1)  to execute in the order we want
@pytest.mark.asyncio(scope="session")
async def test_get_events(default_client: httpx.AsyncClient, mock_event: Event) -> None:
    response = await default_client.get("/event/")

    assert response.status_code == 200
    assert response.json()[0]["_id"] == str(mock_event.id)


@pytest.mark.asyncio(scope="session")
async def test_get_event(default_client: httpx.AsyncClient, mock_event: Event) -> None:
    url = f"/event/{str(mock_event.id)}"
    response = await default_client.get(url)

    assert response.status_code == 200
    assert response.json()["creator"] == mock_event.creator
    assert response.json()["_id"] == str(mock_event.id)
    assert response.json()['title'] == 'FastAPI Book Launch'


@pytest.mark.asyncio(scope="session")
async def test_post_event(default_client: httpx.AsyncClient, access_token: str) -> None:
    payload = {
        "title": "FastAPI Book Launch",
        "image": "https://linktomyimage.com/image.png",
        "description": "We will be discussing the contents of the FastAPI book in this event.Ensure to come with your own copy to win gifts!",
        "tags": [
            "python",
            "fastapi",
            "book",
            "launch"
        ],
        "location": "Google Meet",
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}"
    }

    test_response = {
        "message": "Event created successfully"
    }

    response = await default_client.post("/event/new", json=payload, headers=headers)

    assert response.status_code == 200
    assert response.json() == test_response


@pytest.mark.asyncio(scope="session")
async def test_get_events_count(default_client: httpx.AsyncClient) -> None:
    response = await default_client.get("/event/")

    events = response.json()
    print(events)
    assert response.status_code == 200
    assert len(events) == 2


@pytest.mark.asyncio(scope="session")
async def test_update_event(default_client: httpx.AsyncClient, mock_event: Event, access_token: str) -> None:
    test_payload = {
        "title": "Updated FastAPI event"
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}"
    }

    url = f"/event/{str(mock_event.id)}"
    print(mock_event.id)

    response = await default_client.put(url, json=test_payload, headers=headers)

    assert response.status_code == 200
    assert response.json()["title"] == test_payload["title"]



@pytest.mark.asyncio(scope="session")
async def test_delete_event(default_client: httpx.AsyncClient, mock_event: Event, access_token: str) -> None:
    test_response = {
        "message": "Event deleted successfully."
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}"
    }

    url = f"/event/{mock_event.id}"

    response = await default_client.delete(url, headers=headers)

    assert response.status_code == 200
    assert response.json() == test_response


@pytest.mark.asyncio(scope="session")
async def test_get_event_again(default_client: httpx.AsyncClient, mock_event: Event) -> None:
    url = f"/event/{str(mock_event.id)}"
    response = await default_client.get(url)

    assert response.status_code == 404



"""
-pip install coverage 
-coverage run -m pytest = to run everything
-coverage report = to see the results, SO WE MUST EXECUTE 'coverage run -m pytest'
-pip install pytest-ordering = installation of ordering, pytests library to set the order which modules are 
executed. (@pytest.mark.run(order=<number of order, starting from 1>))
"""


"""
IF THE FIXTURE SCOPE WERE SET AS session THE mock_event ONLY EXECUTES ON INSTANCE FOR ALL THE TESTS (IN ALL MODULES)
THAT MEANS, THAT IN THE DATABASE ONLY WILL BE CREATED ONE EVENT FOR ALL THE TESTS . 
IN OUR CASE (scope=function) WE'RE CREATING A EVENT FOR EVERY SINGLE TEST, AND THAT'S THE REASON WHY 
WE'RE NOT GETTING THE DESIRED OUTCOMES. AND OF COURSE WE'RE WASTING TIME CREATING AN INSTANCE FOR EVERY TEST.

THE BEHAVIOR WOULD BE THE SAME WITH module, BUT IF WE HAVE THE TESTS SPREADED FOR SEVERAL MODULES, THAT WILL CAUSE
ERROR, BECAUSE THIS SCOPE ONLY APPLIES TO THE CURRENT MODULE
"""


"""pytest -vv <file> = run the test """


"""THE ASYNCHRONOUS TESTS MUST ALSO HAVE THE RESPECTIVE SCOPE AAAAAAAAAAAAAAAAAAAAHHHHHHHHHHHHHHHHHHH"""