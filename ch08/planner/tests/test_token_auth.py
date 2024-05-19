import httpx
import pytest
from planner.routes.events import Event

@pytest.mark.asyncio(scope='session')
async def test_wrong_token(default_client: httpx.AsyncClient, mock_event: Event) -> None:
    test_payload = {
        "title": "Invalid token"
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer wrongtokeninformation"
    }

    url = f"/event/{str(mock_event.id)}"

    response = await default_client.put(url, json=test_payload, headers=headers)

    assert response.status_code == 400
    assert response.json()['detail'] == test_payload["title"]


@pytest.mark.asyncio(scope='session')
async def test_empty_token(default_client: httpx.AsyncClient) -> None:
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
        "accept": "application/json",
        "content-type": "application/json",
        "Authorization": "Bearer" # If this header is not provided, oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/user/signin")
        # will raise '401 unauthorized'.
        # while if the token is empty (like our assert) the conditional in the 'authenticate' will act. 
    }

    response = await default_client.post('/event/new', json=payload, headers=headers)

    assert response.status_code == 403
    assert response.json()['detail'] == 'Sign in for access'

