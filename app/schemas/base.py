from pydantic import BaseModel

class LoginRequest(BaseModel):
    email: str
    password: str
    
class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str
    expires_in: int
    
class LoginResponse(BaseModel):
    user_id: int
    username: str
    email: str
    full_name: str
    role: str
    token: TokenResponse