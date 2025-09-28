from fastapi import APIRouter
from fastapi import APIRouter
from app.administrator.api.v1.services import auth

router = APIRouter()

router.include_router(auth.router,tags=["auth"])