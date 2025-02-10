import logging
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from services.indicators_service import IndicatorsService
from schema.responses.indicators_responses import (
    IndicatorSearchResponseModel,
    IndicatorDetailsCustomResponseModel,
)
from models.indicators_model import LANGUAGE
from config.db_config import get_db
from utils.logger import setup_logger

logger = setup_logger(__name__, level=logging.INFO)

router = APIRouter()
indicators_service = IndicatorsService()


@router.get(
    "/indicators/search",
    response_model=list[IndicatorSearchResponseModel],
    description="Search for indicators based on a keyword, with optional language and result limit."
)
async def search_indicators(
    query: str = None,
    limit: int = 10,
    lang: LANGUAGE = LANGUAGE.EN,
    db: Session = Depends(get_db)
):
    logger.info(
        f"Searching indicators with query: {query}, limit: {limit}, lang: {lang}")
    try:
        response = indicators_service.search_indicators(query, limit, lang, db)

        if not response:
            logger.warning("No indicators found for the provided query.")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No indicators found for the specified query."
            )

        logger.info(f"Found {len(response)} indicators for query: {query}")
        return response

    except HTTPException as http_exc:
        if http_exc.status_code == status.HTTP_404_NOT_FOUND:
            raise http_exc
        logger.error(
            f"HTTP error occurred while searching indicators: {http_exc}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred. Please try again later."
        )
    except Exception as e:
        logger.error(
            f"Unexpected error occurred while searching indicators: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred. Please try again later."
        )


@router.get(
    "/indicators/{indicator_code}",
    response_model=IndicatorDetailsCustomResponseModel,
    description="Retrieve detailed data for a specific indicator and entity."
)
async def get_indicator_details(
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
