from fastapi import FastAPI
from app.core.config import configure_app
from app.api import users, pets

app = FastAPI(title="Monolito: Usuarios y Mascotas")

configure_app(app)

app.include_router(users.router, prefix="/api/users", tags=["users"])
app.include_router(pets.router, prefix="/api/pets", tags=["pets"])
