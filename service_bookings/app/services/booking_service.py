from app.models.schemas import Booking, BookingBase
from app.core.messaging import publish_to_queue
from fastapi import HTTPException

class BookingService:
    def __init__(self):
        self.bookings_db: dict[int, Booking] = {}
        self.booking_id_counter = 0

    def create_booking(self, booking_in: BookingBase) -> Booking:
        self.booking_id_counter += 1
        new_booking = Booking(id=self.booking_id_counter, **booking_in.dict())
        self.bookings_db[self.booking_id_counter] = new_booking

        # Enviar a RabbitMQ
        publish_to_queue(new_booking.dict())

        return new_booking

    def get_booking(self, booking_id: int) -> Booking:
        if booking_id not in self.bookings_db:
            raise HTTPException(status_code=404, detail="Booking not found")
        return self.bookings_db[booking_id]

    def get_all_bookings(self) -> list[Booking]:
        return list(self.bookings_db.values())
