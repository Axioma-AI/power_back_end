import logging
from functools import cache
from pydantic_settings import BaseSettings
from src.utils.logger import setup_logger

logger = setup_logger(__name__, level=logging.DEBUG)

class Settings(BaseSettings):
    service_name: str = "Backend de AXIOMA"
    k_revision: str = "local"
    log_level: str = "DEBUG"
    api_url: str = "http://localhost:8000/"

    db_host: str = "localhost"
    db_user: str = "root"
    db_password: str = "root"
    db_port: int = 3306
    db_name: str = "axioma"

    # vector_database_host: str = "localhost"
    # vector_database_port: int = 8000

    firebase_type: str
    firebase_project_id: str
    firebase_private_key_id: str
    firebase_private_key: str
    firebase_client_email: str
    firebase_client_id: str
    firebase_auth_uri: str
    firebase_token_uri: str
    firebase_auth_provider_x509_cert_url: str
    firebase_client_x509_cert_url: str
    firebase_universe_domain: str
    firebase_database_url: str 

    class Config:
        env_file = ".env"

@cache
def get_settings():
    return Settings()
