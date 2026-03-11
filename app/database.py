import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# 1. Load enviroment variables from .env file
load_dotenv()

# 2. Get the Database URL from the enviroment
# Default to a local SQLite file if no URL is provided
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///.journal.db")

# 3. Create the Engine
if SQLALCHEMY_DATABASE_URL.startswith("sqlite"):
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
    )
else:
    engine = create_engine(SQLALCHEMY_DATABASE_URL)

# 4. Create the Session class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 5. Create the Base class
Base = declarative_base()

# 6. Dependency to get the DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()