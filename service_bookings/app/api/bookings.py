from fastapi import APIRouter
from typing import List
from app.models.schemas import Booking, BookingBase
from app.services.booking_service import BookingService

router = APIRouter()
booking_service = BookingService()

@router.post("/", response_model=Booking, status_code=201)
def create_booking(booking_in: BookingBase):
    return booking_service.create_booking(booking_in)

@router.get("/{booking_id}", response_model=Booking)
def get_booking(booking_id: int):
    return booking_service.get_booking(booking_id)

@router.get("/", response_model=List[Booking])
def get_all_bookings():
    return booking_service.get_all_bookings()
