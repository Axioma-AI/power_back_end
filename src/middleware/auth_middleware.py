import logging
import traceback
from typing import Callable
from fastapi import Request, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from src.services.auth_service import AuthService
from src.config.db_config import get_db
from functools import wraps
from src.schema.auth_schemas import User
from src.utils.logger import setup_logger

security = HTTPBearer()
logger = setup_logger(__name__, level=logging.INFO)


def verify_token(func: Callable) -> Callable:
    @wraps(func)
    async def wrapper(*args, **kwargs):
        # Get request from kwargs instead of args
        request = kwargs.get('request')

        if not request or not isinstance(request, Request):
            logger.error(f"Request not found in kwargs: {kwargs}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Request object not found"
            )

        try:
            # Extract token from Authorization header
            credentials: HTTPAuthorizationCredentials = await security(request)
            if not credentials:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Bearer token missing"
                )

            # Verify token using existing AuthService
            token = credentials.credentials
            decoded_token = await AuthService.validate_token(token)

            # Create user if not exists using Firebase user info
            user_info = User(
                email=decoded_token.get('email'),
                name=decoded_token.get('name'),
                picture=decoded_token.get('picture'),
                email_verified=decoded_token.get('email_verified', False),
                phone=decoded_token.get('phone_number', None),
            )

            # Get database session
            db = next(get_db())

            # Get or create user in database
            user = await AuthService.get_or_create_user(db, user_info)

            # Add both decoded token and database user to request state
            request.state.user = decoded_token
            request.state.db_user = user

            return await func(*args, **kwargs)

        except HTTPException as e:
            logger.error(
                f"HTTP error occurred while verifying token: {e}\nTraceback:\n{traceback.format_exc()}")
            raise e
        except Exception as e:
            logger.error(
                f"Error occurred while verifying token: {e}\nTraceback:\n{traceback.format_exc()}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Invalid authentication credentials: {str(e)}"
            )

    return wrapper
