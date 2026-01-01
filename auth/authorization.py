from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import Annotated
from fastapi import Depends

ouath_schem = OAuth2PasswordBearer(
    tokenUrl="token",
    refreshUrl="refresh",
    scheme_name="login",
    description="Autenticate user by email and password",   
)


AuthType = Annotated[str, ouath_schem]
AuthFormType = Annotated[OAuth2PasswordRequestForm, Depends()]