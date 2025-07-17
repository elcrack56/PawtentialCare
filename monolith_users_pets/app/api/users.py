from fastapi import APIRouter, Depends
from typing import List
from app.models.schemas import User, UserCreate
from app.services.user_service import UserService

router = APIRouter()
user_service = UserService()

@router.post("/", response_model=User, status_code=201)
def create_user(user_in: UserCreate):
    return user_service.create_user(user_in)

@router.get("/{user_id}", response_model=User)
def get_user(user_id: int):
    return user_service.get_user(user_id)

@router.get("/", response_model=List[User])
def get_all_users():
    return user_service.get_all_users()
