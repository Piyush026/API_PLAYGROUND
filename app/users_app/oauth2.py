from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from app.users_app.token import verify_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/token/")


def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    user = verify_token(token)
    if user is None:
        raise credentials_exception
    return user
