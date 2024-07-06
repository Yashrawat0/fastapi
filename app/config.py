#This file is handing the validation for the env variable that this project required 
from pydantic_settings import BaseSettings

class Setting(BaseSettings):
    database_hostname: str
    database_port: str
    database_password: str
    database_name: str
    database_username: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    class Config:   # importing .env file into the class
        env_file = ".env"


settings = Setting()


