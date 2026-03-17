from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta
from jose import jwt, JWTError

from . import crud, models, schemas, database, security

# This creates the database tables if they don't exist yet
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(
    title="Personal Journal API",
    description="A secure, full-stack journaling application.",
    version="0.1.0"
)

# ==========================================
# SECURITY DEPENDENCIES
# ==========================================

# This single line tells FastAPI exactly where users go to log in.
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    """This function is the 'Bouncer' for protected routes."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        # 1. Open the JWT token and read the data inside
        payloan = jwt.decode(token, security.SECRET_KEY,
                             algorithms=[security.ALGORITHM])
        username: str = payloan.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        # If the token is fake, expired, or tampered with, kick them out
        raise credentials_exception

    # 2. Look up the user in the database
    user = crud.get_user_by_username(db, username=username)
    if user is None:
        raise credentials_exception
    return user

# ==========================================
# AUTHENTICATION ROUTES
# ==========================================


@app.post("/token")
def login_for_access_token(from_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    """Receives a username & password, returns a JWT token if they match."""

    # 1. Find the user
    user = crud.get_user_by_username(db, username=from_data.username)

    # 2. Verify the password
    if not user or not security.verify_password(from_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"}
        )

    # 3. Create the token
    access_token_expires = timedelta(minutes=security.ACCESS_TOKEN_EXPIRE)
    access_token = security.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

# ==========================================
# USER ROUTES
# ==========================================


@app.post("/users/", response_model=schemas.User, status_code=status.HTTP_201_CREATED)
def register_user(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    """
    1. Check if user already exists.
    2. If not, create them in the database.
    3. Return the user (excluding the password).
    """
    # Check for existing email
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(
            status_code=400,
            detail="Email alrteady registered"
        )
    # Check for existing username
    db_username = crud.get_user_by_username(db, username=user.username)
    if db_username:
        raise HTTPException(
            status_code=400,
            detail="Username already taken"
        )
    return crud.create_user(db=db, user=user)


@app.get("/users/me", response_model=schemas.User)
def read_user_profile(current_user: schemas.User = Depends(get_current_user)):
    """Fetches the profile of the currently logged-in user."""
    return current_user
