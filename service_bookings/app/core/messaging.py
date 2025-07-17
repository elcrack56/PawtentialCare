import pika
import json

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
