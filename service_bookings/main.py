import pika
import json
from fastapi import FastAPI, HTTPException
import schemas

app = FastAPI(title="Microservicio: Reservas")

bookings_db: dict[int, schemas.Booking] = {}
booking_id_counter = 0

def publish_to_queue(booking_data: dict):
    try:
        credentials = pika.PlainCredentials('user', 'password')
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='rabbitmq', credentials=credentials)
        )
        
        channel = connection.channel()
        channel.queue_declare(queue='booking_notifications', durable=True)
        
        message_body = json.dumps(booking_data, default=str)

        channel.basic_publish(
            exchange='',
            routing_key='booking_notifications',
            body=message_body,
            properties=pika.BasicProperties(
                delivery_mode=2,
            ))
        print(f"[✅] Mensaje de reserva #{booking_data.get('id')} enviado a la cola con éxito.")
        connection.close()
    except Exception as e:
        print(f"[❌] ERROR publicando en RabbitMQ: {e}")

@app.post("/api/bookings", response_model=schemas.Booking, status_code=201)
def create_booking(booking_in: schemas.BookingBase):
    global booking_id_counter
    booking_id_counter += 1
    
    new_booking = schemas.Booking(id=booking_id_counter, **booking_in.dict())
    bookings_db[booking_id_counter] = new_booking
    
    publish_to_queue(new_booking.dict())
    
    return new_booking

@app.get("/api/bookings/{booking_id}", response_model=schemas.Booking)
def get_booking(booking_id: int):
    if booking_id not in bookings_db:
        raise HTTPException(status_code=404, detail="Booking not found")
    return bookings_db[booking_id]