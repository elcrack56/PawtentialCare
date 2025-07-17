import pika
import json
import time
from service.notification_service import NotificationService

CREDENTIALS = pika.PlainCredentials('user', 'password')
CONNECTION_PARAMS = pika.ConnectionParameters(host='rabbitmq', credentials=CREDENTIALS)
QUEUE_NAME = 'booking_notifications'

def start_consumer():
    connection = None
    while not connection:
        try:
            connection = pika.BlockingConnection(CONNECTION_PARAMS)
            print("[✅] Conexión con RabbitMQ establecida con éxito.")
        except pika.exceptions.AMQPConnectionError as e:
            print(f"[❌] No se pudo conectar a RabbitMQ ({e}). Reintentando en 5 segundos...")
            time.sleep(5)

    channel = connection.channel()
    channel.queue_declare(queue=QUEUE_NAME, durable=True)

    def callback(ch, method, properties, body):
        message = json.loads(body)
        NotificationService().handle_notification(message)
        ch.basic_ack(delivery_tag=method.delivery_tag)

    channel.basic_consume(queue=QUEUE_NAME, on_message_callback=callback)

    print("\n[*] El Servicio de Notificaciones está esperando mensajes. Presiona CTRL+C para salir.")
    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        print("Interrumpido por el usuario.")
        connection.close()
