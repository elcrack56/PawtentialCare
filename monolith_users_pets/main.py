from fastapi import FastAPI, HTTPException
import schemas

app = FastAPI()
users_db = {}
user_id_counter = 0

@app.post("/api/users", response_model=schemas.User)
def create_user(user_in: schemas.UserCreate):
    global user_id_counter
    user_id_counter += 1
    new_user = schemas.User(id=user_id_counter, **user_in.dict(), pets=[])
    users_db[user_id_counter] = new_user
    return new_user

@app.get("/api/users")
def get_all_users():
    return list(users_db.values())
