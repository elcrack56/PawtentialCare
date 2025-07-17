from fastapi import APIRouter
from typing import List
from app.models.schemas import Pet, PetBase
from app.services.pet_service import PetService
from app.services.user_service import UserService

router = APIRouter()
user_service = UserService()
pet_service = PetService(user_service)

@router.post("/", response_model=Pet, status_code=201)
def create_pet(pet_in: PetBase):
    return pet_service.create_pet(pet_in)

@router.get("/", response_model=List[Pet])
def get_all_pets():
    return pet_service.get_all_pets()
