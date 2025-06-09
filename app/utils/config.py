from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    google_client_id: str
    google_client_secret: str
    google_redirect_uri: str
    google_auth_url: str
    google_token_url: str
    google_user_info_url: str

    redis_host: str
    redis_port: int

    class Config:
        env_file = "app/.env"

settings = Settings()
