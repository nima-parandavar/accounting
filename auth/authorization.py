from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import Annotated
from fastapi import Depends, status
from fastapi.exceptions import HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from core.jwt import JWT

oauth_scheme = OAuth2PasswordBearer(
    tokenUrl="token",
    scheme_name="login",
    description="Authenticated user by email and password",
)

AuthType = Annotated[str, oauth_scheme]
AuthFormType = Annotated[OAuth2PasswordRequestForm, Depends()]

security = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> str:
    jwt = JWT()
    token = credentials.credentials
    payload = jwt.verify_token(token)
    
    if not payload:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid token")
    
    return payload.id


CurrentUserType = Annotated[str, Depends(get_current_user)]
