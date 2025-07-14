from pydantic import BaseModel
from datetime import date

class BookingBase(BaseModel):
    user_id: int
    pet_id: int
    start_date: date
    end_date: date

class Booking(BookingBase):
    id: int
    status: str = "pending"