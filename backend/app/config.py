from pydantic import BaseSettings


class Settings(BaseSettings):
    PORT: int = 8000
    MONGODB_URI: str = "mongodb://localhost:27017/"
    DB_NAME: str = "MR_DEV"
    SECRET_KEY: str = "my_secret_key"
    ALGORITHM: str = "HS256"
    TOKEN_EXPIRE_MINUTES: int = 30


settings = Settings()
