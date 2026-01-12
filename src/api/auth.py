from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from src.database import get_session
from src.models import User
from src.security import get_password_hash, create_access_token, verify_password
from sqlmodel import SQLModel
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter()

# Schema for incoming registration data
class UserCreate(SQLModel):
    email: str
    password: str

# Schema for token response
class Token(SQLModel):
    access_token: str
    token_type: str = "bearer"

@router.post("/register", response_model=Token)
def register_user(user: UserCreate, session: Session = Depends(get_session)):
    # Check if email already exists
    db_user = session.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User already exist please login."
        )
    
    # Hash password
    hashed_password = get_password_hash(user.password)
    new_user = User(email=user.email, password_hash=hashed_password)
    
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    
    # Create JWT token
    access_token = create_access_token(data={"sub": new_user.email})
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/login", response_model=Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_session)):
    user = session.query(User).filter(User.email == form_data.username).first()
    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}
