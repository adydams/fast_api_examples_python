from pydantic import BaseSettings
from dotenv import load_dotenv
from pathlib import Path
import os


#setting path in environment variables
class Settings(BaseSettings):
    database_hostname: str = ""
    database_port:str = ""
    database_password: str  = ""
    database_name: str  = ""
    database_username: str = ""
    secret_key: str  = ""
    algorithm: str = ""
    access_token_expire_minute: int = 0

    #getting values form config file
    class Config:
        env_file = '~/.env'
settings = Settings()