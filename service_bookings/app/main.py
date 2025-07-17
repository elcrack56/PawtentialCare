from fastapi import FastAPI
from app.api.bookings import router as bookings_router

app = FastAPI(title="Microservicio: Reservas")

app.include_router(bookings_router, prefix="/api/bookings", tags=["bookings"])
