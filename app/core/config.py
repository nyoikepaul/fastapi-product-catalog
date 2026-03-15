from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class Settings(BaseSettings):
    PROJECT_NAME: str = "Secure Product Catalog"
    # Provide a default for local dev/testing to prevent ValidationErrors
    API_KEY: str = "dev_key_placeholder"
    DATABASE_URL: str = "sqlite:///./test.db"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
