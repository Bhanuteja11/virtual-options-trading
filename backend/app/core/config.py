from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name: str = "Virtual Options Trading API"
    environment: str = "dev"

settings = Settings()
