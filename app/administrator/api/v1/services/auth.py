from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from app.core.deps import get_db
from app.models.base import User
from app.core.security import create_access_token, verify_password, create_refresh_token
from app.core.config import settings
from app.schemas.base import LoginRequest, TokenResponse, LoginResponse
from app.utils.decrypt_password import decrypt_password

router = APIRouter()

@router.post("/login")
def login(data: LoginRequest, db: Session = Depends(get_db)) -> JSONResponse:
    
    """
    authentication endpoint for users
    :param data: LoginRequest
    :return: JSONResponse
    """
    
    user = db.query(User).filter(User.email == data.email).first()

    if not user:
        return JSONResponse(
            status_code=401,
            content={
                "result": "failure",
                "error_message": "Invalid email address or password"
            }
        )

    try:
        decrypted_password = decrypt_password(data.password)
    except Exception as e:
        return JSONResponse(
            status_code=400,
            content={
                "result": "failure",
                "error_message": f"Password decryption failed: {e}"
            }
        )

    if not verify_password(decrypted_password, user.password):
        return JSONResponse(
            status_code=401,
            content={
                "result": "failure",
                "error_message": "Invalid email address or password"
            }
        )

    access_token = create_access_token({"sub": str(user.id)})
    refresh_token = create_access_token({"sub": str(user.id)})

    token_response = TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer",
        expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )

    response = LoginResponse(
        user_id=user.id,
        username=user.username,
        email=user.email,
        full_name=user.full_name,
        role=user.role,
        token=token_response
    )

    return JSONResponse(
        status_code=200,
        content={
            "result": "success",
            "response": response.dict()   # convert Pydantic model to dict
        }
    )

    