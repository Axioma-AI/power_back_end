import logging
from fastapi import FastAPI
from src.config.config import get_settings
from src.config.cors_config import add_cors
from src.routes.api.v1 import router as v1_router
from src.utils.logger import setup_logger
from contextlib import asynccontextmanager
from src.services.firebase_service import initialize_firebase
from firebase_admin import delete_app, get_app

logger = setup_logger(__name__, level=logging.INFO)

_SETTINGS = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        initialize_firebase()
        yield
    finally:
        logger.info("Shutting down Firebase Admin SDK")
        delete_app(get_app())

app = FastAPI(
    title=_SETTINGS.service_name,
    version=_SETTINGS.k_revision,
    level=_SETTINGS.log_level,
    lifespan=lifespan,
)


add_cors(app)

# Include the routes with versioning
app.include_router(v1_router, prefix="/api/v1")

if __name__ == "__main__":
    import uvicorn
    logger.info("Starting the application...")
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
