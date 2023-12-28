from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Users
from fastapi.security import OAuth2PasswordRequestForm
router = APIRouter()

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

class CreateUserRequest(BaseModel):
    username : str
    email : str
    first_name : str
    last_name : str
    password : str
    role : str

def authenticate_user(db : db_dependency, username : str, password : str):
    user = db.query(Users).filter(Users.username == username).first()
    if user is None:
        return False
    if not bcrypt_context.verify(password, user.hashed_password):
        return False
    return user

@router.post("/auth/", status_code=status.HTTP_201_CREATED)
async def create_user(db: db_dependency , create_user_request : CreateUserRequest):
    user_model = Users(
        email = create_user_request.email,
        username = create_user_request.username,
        first_name = create_user_request.first_name,
        last_name = create_user_request.last_name,
        hashed_password = bcrypt_context.hash(create_user_request.password),
        role = create_user_request.role,
        is_active = True
    )
    db.add(user_model)
    db.commit()
    return {"message" : "User created successfully"}

@router.post("/token", status_code=status.HTTP_201_CREATED)
async def login_for_access_token(form_data : Annotated[OAuth2PasswordRequestForm, Depends()], db : db_dependency):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password")
    return 'Successful authentication'