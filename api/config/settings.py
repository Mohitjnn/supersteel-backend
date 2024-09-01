from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str
    mongo_url: str

    class Config:
        env_file = ".env"
