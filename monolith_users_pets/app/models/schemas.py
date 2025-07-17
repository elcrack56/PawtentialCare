from pydantic import BaseModel, EmailStr
from typing import List

class PetBase(BaseModel):
    name: str
    species: str
    owner_id: int

class Pet(PetBase):
    id: int

class UserBase(BaseModel):
    email: EmailStr
    full_name: str

class UserCreate(UserBase):
    pass

class User(UserBase):
    id: int
    pets: List[Pet] = []
