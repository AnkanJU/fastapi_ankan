from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    APP_NAME: str = "FastAPI App"
    DATABASE_URL: str = "sqlite:///./todos.db"
    DEBUG_MODE: bool = False
    
    # JWT Configuration
    SECRET_KEY: str = "super_secret_jwt_key_change_this_in_production_123456"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

settings = Settings()