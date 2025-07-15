from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
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

app = FastAPI()
users_db = {}
user_id_counter = 0

@app.post("/api/users", response_model=schemas.User)
def create_user(user_in: schemas.UserCreate):
    global user_id_counter
    for user in users_db.values():
        if user.email == user_in.email:  
            raise HTTPException(status_code=400, detail="Email already registered")

    user_id_counter += 1
    new_user = schemas.User(id=user_id_counter, **user_in.dict(), pets=[])
    users_db[user_id_counter] = new_user
    return new_user


@app.get("/api/users")
def get_all_users():
    return list(users_db.values())
