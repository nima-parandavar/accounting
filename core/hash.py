from passlib.context import CryptContext
from config.settings import app_settings

class Hash():
    def __init__(self, schemas: list[str] | None = None):
        self.__schemas = schemas if schemas else app_settings.schemas

        if not self.__schemas:
            raise ValueError("schemas must be set")

        self.__ctx = CryptContext(schemes=self.__schemas)
    
    def make_hash(self, value: str) -> str:
        return self.__ctx.hash(value)
    
    def verify(self, hash_value: str, raw_value: str) -> bool:
        return self.__ctx.verify(raw_value, hash_value)