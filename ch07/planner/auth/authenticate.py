from planner.auth.jwt_handler import verify_access_token
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/user/signin")


async def authenticate(token: str = Depends(oauth2_scheme)) -> str: 
    # Depends first executes the function and then, the returned values are passed to 'token'
    # which must be correct with its dependency injection, which, in this case is 'str'
    # but most of the time could be an object such as classes.
    # SO, THE RETURN VALUE MUST FIT THE DEPENDENCY INJECTION NECESSITY.
    if not token:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Sign in for access"
        )

    decoded_token = verify_access_token(token)
    return decoded_token["user"]

