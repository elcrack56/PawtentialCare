from app.models.schemas import User, UserCreate, Pet
from fastapi import HTTPException

class UserService:
    def __init__(self):
        self.users_db: dict[int, User] = {}
        self.user_id_counter = 0

    def create_user(self, user_in: UserCreate) -> User:
        for user in self.users_db.values():
            if user.email == user_in.email:
                raise HTTPException(status_code=400, detail="Email already registered")
        self.user_id_counter += 1
        new_user = User(id=self.user_id_counter, **user_in.dict(), pets=[])
        self.users_db[self.user_id_counter] = new_user
        return new_user

    def get_user(self, user_id: int) -> User:
        if user_id not in self.users_db:
            raise HTTPException(status_code=404, detail="User not found")
        return self.users_db[user_id]

    def get_all_users(self) -> list[User]:
        return list(self.users_db.values())
