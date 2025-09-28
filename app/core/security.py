from passlib.context import CryptContext
from typing import Optional
from jose import JWTError, jwt
from app.core.config import settings
from datetime import datetime,timedelta, timezone

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password:str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password:str, hashed_password:str) -> bool:
    return pwd_context.verify(plain_password,hashed_password)


# JWT token creation
def create_access_token(data:dict, expires_delta:Optional[int] = None) -> str:
    """
    Create an access token for user authentication.
    Args:
        data (dict): Data to include in the token payload.
        expires_delta (Optional[int]): Expiration time delta in seconds.
    Returns:
        str: Encoded JWT token.
    """
    
    to_encode = data.copy()
    
    expire = datetime.now(timezone.utc) + timedelta(minutes=expires_delta or settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp":expire})
    
    return jwt.encode(to_encode,settings.SECRET_KEY,algorithm=settings.ALGORITHM)

def create_refresh_token(data: dict):
    # Use a longer expiry for refresh token
    expire = datetime.now(timezone.utc) + timedelta(days=7)  # Example: 7 days
    to_encode = data.copy()
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def decode_access_token(token:str) -> dict:
    
    """
    Decode an access token and extract its payload.
    Args:
        token (str): Access token to decode.
    Returns:
        dict: Decoded token payload.
    Raises:
        Exception: If the token is invalid.
    """
    
    try:
        payload = jwt.decode(token,settings.SECRET_KEY,algorithms=[settings.ALGORITHM])
        return payload
    except JWTError:
        raise Exception("Invalid Token")
    

