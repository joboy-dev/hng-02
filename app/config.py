from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    '''Configuration for environment variables'''

    secret_key: str
    algorithm: str
    access_token_expire_hours: int

    hostname: str
    db_name: str
    user: str
    password: str
    db_port: int

    class Config:
        env_file = '.env'


settings = Settings()
