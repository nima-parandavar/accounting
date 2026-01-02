from jwt import encode as py_encode, decode as py_decode
from jwt.exceptions import (
    PyJWTError,
    ExpiredSignatureError,
    InvalidAlgorithmError,
    InvalidKeyError,
)
from config.settings import app_settings
from fastapi.exceptions import HTTPException
from fastapi import status
from pydantic import BaseModel


class Payload(BaseModel):
    id: str
    exp: float


class JWT:
    def __init__(
        self,
        algorithm: str | None = None,
        expire_token_minute: int | None = None,
    ):
        self.algorithm = algorithm if algorithm else app_settings.algorithm
        self.expire_token_minute = (
            expire_token_minute
            if expire_token_minute
            else app_settings.access_token_expire_minutes
        )
        self.__secret_key = app_settings.secret_key

        if not self.algorithm:
            raise InvalidAlgorithmError(
                "algorithm must be set",
            )

        if not self.expire_token_minute:
            raise ValueError("expire_token_minute must be set")

        if not self.__secret_key:
            raise ValueError("Set SECRET_KEY variable in environment file")

    def encode(self, payload: Payload) -> str:
        return py_encode(payload, self.__secret_key, self.algorithm)

    def decode(self, token: str) -> Payload:

        payload = py_decode(
            token,
            self.__secret_key,
            self.algorithm,
            options={"require": ["exp", "id"]},
            leeway=5
        )
        return Payload(**payload)

    def verify_token(self, token: str) -> Payload:
        try:
            return self.decode(token)
        except ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired"
            )
        except PyJWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
            )
        except InvalidKeyError:

            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
            )
