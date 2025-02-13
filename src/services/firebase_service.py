import firebase_admin
from firebase_admin import credentials
from src.config.config import get_settings
from src.utils.logger import setup_logger
import logging

logger = setup_logger(__name__, level=logging.INFO)
_SETTINGS = get_settings()


def initialize_firebase():
    """Initialize Firebase Admin SDK"""
    try:
        # First try to get existing app
        firebase_admin.get_app()
    except ValueError:
        # Initialize new app if none exists
        try:
            cred = credentials.Certificate({
                "type": _SETTINGS.firebase_type,
                "project_id": _SETTINGS.firebase_project_id,
                "private_key_id": _SETTINGS.firebase_private_key_id,
                "private_key": _SETTINGS.firebase_private_key.replace("||", "\n"),
                "client_email": _SETTINGS.firebase_client_email,
                "client_id": _SETTINGS.firebase_client_id,
                "auth_uri": _SETTINGS.firebase_auth_uri,
                "token_uri": _SETTINGS.firebase_token_uri,
                "auth_provider_x509_cert_url": _SETTINGS.firebase_auth_provider_x509_cert_url,
                "client_x509_cert_url": _SETTINGS.firebase_client_x509_cert_url,
            })

            firebase_admin.initialize_app(cred, {
                'databaseURL': _SETTINGS.firebase_database_url
            })
            logger.info("Firebase Admin SDK initialized successfully")
        except Exception as e:
            logger.error(f"Error initializing Firebase Admin SDK: {e}")
            raise
