from app.models.schemas import Pet, PetBase, User
from fastapi import HTTPException

class PetService:
    def __init__(self, user_service):
        self.pets_db: dict[int, Pet] = {}
        self.pet_id_counter = 0
        self.user_service = user_service

    def create_pet(self, pet_in: PetBase) -> Pet:
        owner = self.user_service.get_user(pet_in.owner_id)
        self.pet_id_counter += 1
        new_pet = Pet(id=self.pet_id_counter, **pet_in.dict())
        self.pets_db[self.pet_id_counter] = new_pet
        owner.pets.append(new_pet)
        return new_pet

    def get_all_pets(self) -> list[Pet]:
        return list(self.pets_db.values())
