import logging
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from src.services.encaje_legal_service import EncajeLegalService
from src.schema.responses.response_encaje_legal_models import EncajeLegalGroupedResponseModel
from src.schema.examples.response_encaje_legal_examples import encaje_legal_responses
from src.config.db_config import get_db
from src.utils.logger import setup_logger

logger = setup_logger(__name__, level=logging.INFO)

router = APIRouter()
encaje_legal_service = EncajeLegalService()

@router.get(
    "/encaje-legal",
    response_model=EncajeLegalGroupedResponseModel,
    responses=encaje_legal_responses,
    description="Retrieve grouped records from 'encaje_legal' table. The values are expressed in thousands of Bolivianos."
)
async def get_encaje_legal_data(db: Session = Depends(get_db)):
    logger.info("Received request for grouped 'encaje_legal' records.")
    try:
        response = encaje_legal_service.get_grouped_entries_by_date(db)
        
        if not response.get("fecha_corte"):
            logger.warning("No records found in 'encaje_legal' for the specified query.")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No records found in encaje_legal for the specified query."
            )
        
        logger.info("Successfully retrieved and grouped 'encaje_legal' records.")
        return response
    
    except HTTPException as http_exc:
        logger.error(f"HTTPException occurred: {http_exc.detail}")
        raise http_exc
    
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred. Please try again later."
        )
