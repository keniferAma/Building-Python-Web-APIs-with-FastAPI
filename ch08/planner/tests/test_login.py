import httpx
import pytest


@pytest.mark.asyncio(scope='session') # this mark.asyncio informs pytest to trear this as an async test. 
                     #ONLY PERFORMED BY event loops
async def test_sign_new_user(default_client: httpx.AsyncClient) -> None:
    payload = {
        "email": "testuser@packt.com",
        "password": "testpassword",
    }

    headers = {
        "accept": "application/json",
        "Content-Type": "application/json"
    }

    test_response = {
        "message": "User created successfully"
    }

    response = await default_client.post("/user/signup", json=payload, headers=headers)

    assert response.status_code == 200
    assert response.json() == test_response


@pytest.mark.asyncio(scope='session')
async def test_user_already_exist(default_client: httpx.AsyncClient) -> None:
    payload = {
        "email": "testuser@packt.com",
        "password": "testpassword"
    }
    
    headers = {
        "accept": "application/json",
        "content-type": "application/json"
    }

    test_response = {"detail": "User with email provided exists already."}

    response = await default_client.post('/user/signup', json=payload, headers=headers)

    assert response.json()['detail'] == test_response["detail"]
    assert response.status_code == 409


@pytest.mark.asyncio(scope='session')
async def test_wrong_username(default_client: httpx.AsyncClient) -> None:
    payload = {
        "username": "wronguser@packt.com",
        "password": "testpassword"
    }

    headers = {
        "accept": "application/json",
        "Content-Type": "application/x-www-form-urlencoded"
    }

    test_reponse = {
        "detail": "User with email does not exist."
    }

    response = await default_client.post('/user/signin', data=payload, headers=headers)
    # Remember: 'json=' to send json format when we set the Content-Type=application/json
    # 'data=' to send form-encoded information when we set the Content-Type=application/x-www-form-urlencoded

    assert response.status_code == 404
    assert response.json()['detail'] == test_reponse["detail"]


@pytest.mark.asyncio(scope='session')
async def test_invalid_password(default_client: httpx.AsyncClient) -> None:
    payload = {
        "username": "testuser@packt.com",
        "password": "wrongpassword"
    }

    headers = {
        "accept": "application/json",
        "Content-Type": "application/x-www-form-urlencoded"
    }

    test_response = {
        "detail": "Invalid details passed."
    }

    response = await default_client.post('/user/signin', data=payload, headers=headers)

    assert response.status_code == 401
    assert response.json()['detail'] == test_response["detail"]


@pytest.mark.asyncio(scope='session')
async def test_sign_user_in(default_client: httpx.AsyncClient) -> None:
    payload = {
        "username": "testuser@packt.com",
        "password": "testpassword"
    }

    headers = {         
        "accept": "application/json",
        "Content-Type": "application/x-www-form-urlencoded"
    }

    response = await default_client.post("/user/signin", data=payload, headers=headers)
    # The event loop scoped by session closed right here and there was not loop from here downwards
    
    assert response.status_code == 200
    assert response.json()["token_type"] == "Bearer"
