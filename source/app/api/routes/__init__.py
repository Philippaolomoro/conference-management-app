from fastapi import APIRouter

from app.api.routes.conference import router as conference_router
from app.api.routes.talk import router as talk_router

router = APIRouter()

router.include_router(conference_router, prefix="/conference", tags=["conference"])
router.include_router(talk_router, prefix="/talk", tags=["talk"])
