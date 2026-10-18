from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    APP_NAME: str = "recall-talk"
    DATABASE_URL: str 
    ECHO_SQL: bool = False

    JWT_SECRET_KEY: str = "super-secret-key-change-in-production-recall-talk-2026"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24

    model_config = SettingsConfigDict(env_file=".env", extra="ignore", env_file_encoding="utf-8")

settings = Settings()