import logging
import traceback
from fastapi import APIRouter, Depends, HTTPException, status, Query, Request
from sqlalchemy.orm import Session
from src.models.user_model import UserModel
from src.services.indicators_service import IndicatorsService
from src.schema.responses.indicators_responses import (
    IndicatorDetailsCustomResponseModelList,
    IndicatorSearchResponseModel,
    IndicatorDetailsCustomResponseModel,
)
from src.models.indicators_model import LANGUAGE
from src.config.db_config import get_db
from src.utils.logger import setup_logger
from src.middleware.auth_middleware import verify_token

logger = setup_logger(__name__, level=logging.INFO)

router = APIRouter()
indicators_service = IndicatorsService()


@router.get(
    "/indicators/search",
    response_model=list[IndicatorSearchResponseModel],
    description="Search for indicators based on a keyword, with optional language and result limit."
)
@verify_token
async def search_indicators(
    request: Request,
    query: str = None,
    limit: int = 10,
    lang: LANGUAGE = LANGUAGE.EN,
    db: Session = Depends(get_db)
):
    logger.info(
        f"Searching indicators with query: {query}, limit: {limit}, lang: {lang}")
    try:
        user: UserModel = request.state.db_user
        response = indicators_service.search_indicators(
            query, limit, lang, db, user.id)

        if response is None:
            logger.warning("No indicators found for the provided query.")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No indicators found for the specified query."
            )
        if not response:
            logger.info(
                "No indicators found for the provided query, returning empty list")
            return []

        logger.info(f"Found {len(response)} indicators for query: {query}")
        return response

    except HTTPException as http_exc:
        if http_exc.status_code == status.HTTP_404_NOT_FOUND:
            raise http_exc
        logger.error(
            f"HTTP error occurred while searching indicators: {http_exc}\nTraceback:\n{traceback.format_exc()}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(http_exc)
        )
    except Exception as e:
        logger.error(
            f"Unexpected error occurred while searching indicators: {e}\nTraceback:\n{traceback.format_exc()}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get(
    "/indicators/{indicator_code}",
    response_model=IndicatorDetailsCustomResponseModel,
    description="Retrieve detailed data for a specific indicator and entity."
)
@verify_token
async def get_indicator_details(
    request: Request,
    indicator_code: str,
    entity_code: str,
    lang: LANGUAGE = LANGUAGE.EN,
    db: Session = Depends(get_db)
):
    logger.info(
        f"Fetching details for indicator: {indicator_code}, entity: {entity_code}, lang: {lang}")
    try:
        response = indicators_service.get_indicator_details(
            indicator_code, entity_code, lang, db)

        if not response:
            logger.warning(
                f"No details found for indicator: {indicator_code} and entity: {entity_code}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No details found for indicator code: {indicator_code} and entity: {entity_code}"
            )

        logger.info(
            f"Successfully retrieved details for indicator: {indicator_code} and entity: {entity_code}")
        return response

    except Exception as e:
        logger.error(f"Unexpected error while fetching indicator details: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred. Please try again later."
        )


@router.get(
    "/indicators/{indicator_code}/entities",
    response_model=IndicatorDetailsCustomResponseModelList,
    description="Retrieve detailed data for a specific indicator across multiple entities."
)
@verify_token
async def get_indicator_details_by_entities(
    request: Request,
    indicator_code: str,
    entity_codes: list[str] = Query(...,
                                    description="List of entity codes to fetch details for"),
    lang: LANGUAGE = LANGUAGE.EN,
    db: Session = Depends(get_db)
):
    logger.info(
        f"Fetching details for indicator: {indicator_code}, entities: {entity_codes}, lang: {lang}")
    try:
        logger.info(f"Entity codes: {entity_codes}")
        logger.info(f"Indicator code: {indicator_code}")
        response = indicators_service.get_indicator_details_by_entities(
            indicator_code, entity_codes, lang, db)

        if not response:
            logger.warning(
                f"No details found for indicator: {indicator_code} and entities: {entity_codes}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No details found for indicator code: {indicator_code} and entities: {entity_codes}"
            )

        logger.info(
            f"Successfully retrieved details for indicator: {indicator_code} and entities: {entity_codes}")
        return response

    except Exception as e:
        logger.error(f"Unexpected error while fetching indicator details: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred. Please try again later."
        )
