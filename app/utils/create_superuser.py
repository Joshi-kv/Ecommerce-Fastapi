import asyncio
from app.models.base import User
from app.core.db import SessionLocal
from app.core.security import get_password_hash
from app.models.base import UserRole

def create_superuser():
    db = SessionLocal()
    try:
        # check if superuser exists
        existing = db.query(User).filter(User.is_superuser == True).first()
        if existing:
            print("Superuser already exists:", existing.username)
            return

        user = User(
            full_name="Admin User",
            username="admin",
            email="admin@example.com",
            password=get_password_hash("Pass@1234"),  # hash password
            mobile_number="9999999999",
            role=UserRole.ADMIN,
            is_active=True,
            is_superuser=True,
            is_email_verified=True,
        )

        db.add(user)
        db.commit()
        db.refresh(user)

        print("Superuser created successfully:", user.username)
    finally:
        db.close()

if __name__ == "__main__":
    create_superuser()