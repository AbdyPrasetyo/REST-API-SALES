from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Using asyncpg for async SQLAlchemy
    DATABASE_URL: str = "postgresql+asyncpg://postgres:spasinya2kali@localhost:5432/sales_db"
    SECRET_KEY: str = "SUPER_SECRET_KEY_2026"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    class Config:
        env_file = ".env"

settings = Settings()