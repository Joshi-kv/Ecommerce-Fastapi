from app.core.db import Base
from sqlalchemy import Column, Integer, DateTime, String, func, Boolean
import enum

class BaseModel(Base):
    __abstract__ = True
    
    create_at = Column(DateTime(timezone=True), server_default=func.now())
    update_at = Column(DateTime(timezone=True), onupdate=func.now())
    

class UserRole(str, enum.Enum):
    ADMIN = 1
    VENDOR = 2
    CUSTOMER = 3
    
class User(BaseModel):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(length=50), nullable=False)
    username = Column(String(length=50), nullable=False, unique=True, index=True)
    email = Column(String(length=50), nullable=False, unique=True, index=True)
    password = Column(String(length=255), nullable=False)
    mobile_number = Column(String(length=50), nullable=False, unique=True, index=True)
    
    role = Column(String(length=50), nullable=False, default=UserRole.CUSTOMER)
    
    is_active = Column(Boolean, default=True)
    is_mobile_verified = Column(Boolean, default=False)
    is_email_verified = Column(Boolean, default=False)
    is_deleted = Column(Boolean, default=False)
    is_superuser = Column(Boolean, default=False)
    
    last_login = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    