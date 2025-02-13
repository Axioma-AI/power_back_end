from . import encaje_legal
from . import indicators
from . import favorites
from fastapi import APIRouter
import sys
import os

sys.path.append(os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../../")))

router = APIRouter()
router.include_router(encaje_legal.router, tags=["Encaje Legal"])
router.include_router(indicators.router, tags=["Indicadores"])
router.include_router(favorites.router, tags=["Favorites"])
