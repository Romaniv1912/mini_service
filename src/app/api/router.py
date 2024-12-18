from fastapi import APIRouter

from src.app.api.ping import router as ping_router
from src.app.api.product import router as product_router

router = APIRouter()

router.include_router(ping_router)
router.include_router(product_router, prefix='/products', tags=['Products'])
