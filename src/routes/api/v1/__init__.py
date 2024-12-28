import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from fastapi import APIRouter
from . import encaje_legal

router = APIRouter()
# router.include_router(articles.router)
router.include_router(encaje_legal.router, tags=["Encaje Legal"])