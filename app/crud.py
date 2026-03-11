from sqlalchemy.orm import Session
from . import models, schemas, security

# ==========================================
# USER OPERATIONS
# ==========================================

def get_user_by_email(db: Session, email: str):
    """READ: Find a user by their email (useful for login/signup validation)."""
    return db.query(models.User).filter(models.User.email == email).first()

def get_user_by_username(db: Session, username: str):
    """READ: Find a user by their username"""
    return db.query(models.User).filter(models.User.username == username).first()

def create_user(db: schemas.UserCreate):
    """CREATE: Securely hash the password and save the new user."""
    # 1. Security: Hash the password IMMEDIATELY
    hashed_pwd = security.get_password_hash(user.password)

    # 2. Database: Create the SQLAlchemy model instance
    db_user = models.User(
        username=user.username
    )