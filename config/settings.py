from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    debug: bool
    db_url: str
    phone_number_region_code: str = "+98"
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int
    schemas: list[str] = ["sha256_crypt"]

    # load env file
    model_config = SettingsConfigDict(env_file=".env")


class FastApiSettings(BaseSettings):
    title: str = "Accounting application"
    version: str = "0.0.0"


app_settings = Settings()
fast_api_settings = FastApiSettings()
