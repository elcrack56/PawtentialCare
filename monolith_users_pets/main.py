from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List
import schemas 

app = FastAPI(title="Monolito: Usuarios y Mascotas")

origins = [
    "http://localhost:3000", 
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

users_db: dict[int, schemas.User] = {}
pets_db: dict[int, schemas.Pet] = {}
user_id_counter = 0
pet_id_counter = 0

@app.post("/api/users", response_model=schemas.User, status_code=201)
def create_user(user_in: schemas.UserCreate):
    global user_id_counter
    for user in users_db.values():
        if user.email == user_in.email:
            raise HTTPException(status_code=400, detail="Email already registered")
    
    user_id_counter += 1
    new_user = schemas.User(id=user_id_counter, **user_in.dict(), pets=[])
    users_db[user_id_counter] = new_user
    print(f"[INFO] Usuario creado en el monolito: {new_user.full_name}")
    return new_user

@app.get("/api/users/{user_id}", response_model=schemas.User)
def get_user(user_id: int):
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    return users_db[user_id]
    
@app.get("/api/users", response_model=List[schemas.User])
def get_all_users():
    return list(users_db.values())

@app.post("/api/pets", response_model=schemas.Pet, status_code=201)
def create_pet(pet_in: schemas.PetBase):
    global pet_id_counter
    owner_id = pet_in.owner_id
    if owner_id not in users_db:
        raise HTTPException(status_code=404, detail=f"Owner with id {owner_id} not found")

    pet_id_counter += 1
    new_pet = schemas.Pet(id=pet_id_counter, **pet_in.dict())
    pets_db[pet_id_counter] = new_pet
    
    users_db[owner_id].pets.append(new_pet)
    
    return new_pet