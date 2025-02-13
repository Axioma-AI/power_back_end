import logging
from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from src.config.db_config import get_db
from src.utils.logger import setup_logger
from src.middleware.auth_middleware import verify_token
from src.services.indicators_service import IndicatorsService
from pydantic import BaseModel

logger = setup_logger(__name__, level=logging.INFO)
router = APIRouter()
indicators_service = IndicatorsService()


class FavoriteToggle(BaseModel):
    indicator_id: int
    is_favorite: bool


@router.post("/favorites/toggle", description="Toggle an indicator as favorite for the current user")
@verify_token
async def toggle_favorite(
    request: Request,
    favorite: FavoriteToggle,
    db: Session = Depends(get_db)
):
    try:
        user = request.state.db_user
        result = await indicators_service.toggle_favorite_indicator(
            db,
            user.id,
            favorite.indicator_id,
            favorite.is_favorite
        )
        return {"success": True, "is_favorite": result}
    except Exception as e:
        logger.error(f"Error toggling favorite: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get("/favorites", description="Get all favorite indicators for the current user")
@verify_token
async def get_favorites(
    request: Request,
    db: Session = Depends(get_db)
):
    try:
        user = request.state.db_user
        favorites = await indicators_service.get_user_favorites(db, user.id)
        return favorites
    except Exception as e:
        logger.error(f"Error getting favorites: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
