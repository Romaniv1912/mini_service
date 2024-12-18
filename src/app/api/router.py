from fastapi import APIRouter

from src.app.api.ping import router as ping_router

router = APIRouter()

router.include_router(ping_router)
