from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    debug: bool
    db_url: str
    phone_number_region_code: str = "+98"

    model_config = SettingsConfigDict(env_file=".env")


class FastApiSettings(BaseSettings):
    pass


app_settings = Settings()
fast_api_settings = FastApiSettings()
