import jwt as pyjwt
from config.settings import app_settings

class JWT:
    def __init__(self, algorithm: str | None, expire_token_minute: int | None):
        self.algorithm = algorithm if algorithm else app_settings.algorithm
        self.expire_token_minute = expire_token_minute if expire_token_minute else app_settings.access_token_expire_minute
        self.__secret_key = app_settings.secret_key

        if not self.algorithm:
            raise pyjwt.exceptions.InvalidAlgorithmError("algorith must be set")
        
        if not self.expire_token_minute:
            raise ValueError("expire_token_minute must be set")
        
        if not self.__secret_key:
            raise ValueError("Set SECRET_KEY variable in envrionment file")
        
    def decode(self, payload: dict) -> str:
        return pyjwt.encode(payload, self.__secret_key, self.algorithm)
    
    def encode(self, token: str) -> dict | bool:
        try:
            payload = pyjwt.decode(
                token,
                self.__secret_key,
                self.algorithm
            )
            return payload
        except pyjwt.exceptions.InvalidKeyError:
            return False
    
        