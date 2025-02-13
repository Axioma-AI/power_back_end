import logging
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from firebase_admin import auth
from src.models.user_model import UserModel
from src.schema.auth_schemas import User
from src.utils.logger import setup_logger

logger = setup_logger(__name__, level=logging.INFO)


class AuthService:
    @staticmethod
    async def validate_token(token: str):
        try:
            decoded_token = auth.verify_id_token(token)
            return decoded_token
        except Exception as e:
            logger.error(f"Error validating token: {e}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token"
            )

    @staticmethod
    async def get_or_create_user(db: Session, user_info: User):
        try:
            # Check if user exists
            user = db.query(UserModel).filter(
                UserModel.email == user_info.email).first()

            if user:
                # Update fields only if they are different
                updated_fields = {
                    "name": user_info.name,
                    "phone": user_info.phone,
                    "picture": user_info.picture,
                    "email_verified": user_info.email_verified,
                    "country_code": user_info.country_code
                }

                changes_made = False
                for field, value in updated_fields.items():
                    if value and getattr(user, field) != value:
                        setattr(user, field, value)
                        changes_made = True

                # Only commit if changes were made
                if changes_made:
                    logger.info(f"Updating user information for {user.email}")
                    db.commit()
                    db.refresh(user)
            else:
                # Create new user
                user = UserModel(
                    email=user_info.email,
                    name=user_info.name,
                    phone=user_info.phone,
                    picture=user_info.picture,
                    email_verified=True,
                    country_code=user_info.country_code
                )
                logger.info(f"Creating new user with email {user_info.email}")
                db.add(user)
                db.commit()
                db.refresh(user)

            return user
        except Exception as e:
            logger.error(f"Error getting or creating social user: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error processing user data"
            )
