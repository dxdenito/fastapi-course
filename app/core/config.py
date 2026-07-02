from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # JWT settings
    secret_key: str = "changeme-before-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    # App settings
    app_name: str = "SteezyFX API"
    debug: bool = True

    model_config = {"env_file": ".env"}


settings = Settings()
