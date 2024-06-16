from pydantic_settings import BaseSettings

from decouple import config


class Settings(BaseSettings):

    # App
    APP_NAME: str = config("APP_NAME")
    DEBUG: bool = config("DEBUG", cast=bool)

    FRONTEND_HOST: str = config("FRONTEND_HOST")

    DATABASE_URI: str = config("DATABASE_URI")

    JWT_SECRET: str = config("JWT_SECRET")
    REFRESH_SECRET: str = config("REFRESH_SECRET")

    JWT_ALGORITHM: str = config("ACCESS_TOKEN_ALGORITHM")

    ACCESS_TOKEN_EXPIRE_MINUTES: int = config(
        "ACCESS_TOKEN_EXPIRE_MINUTES", cast=int
    )
    REFRESH_TOKEN_EXPIRE_MINUTES: int = config(
        "REFRESH_TOKEN_EXPIRE_MINUTES", cast=int
    )

    OPEN_AI_API_KEY: str = config("OPEN_AI_API_KEY")

    PORT: int = config("PORT", cast=int)

    SMTP_HOST: str = config("SMTP_HOST")
    SMTP_PORT: int = config("SMTP_PORT", cast=int)
    SMTP_USERNAME: str = config("SMTP_USERNAME")
    SMTP_PASSWORD: str = config("SMTP_PASSWORD")
