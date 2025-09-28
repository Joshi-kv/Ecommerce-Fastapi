from fastapi import FastAPI, APIRouter
from app.administrator.api.v1.router import router as admin_router
from app.core.config import settings

app = FastAPI(title='Ecommerce API')

app.include_router(
    admin_router,
    prefix=f'{settings.API_V1_STR}/administrator',
    tags=['Administrator']
)
