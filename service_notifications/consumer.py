import pika
import json
import time

# Las credenciales deben coincidir con las de docker-compose.yml
CREDENTIALS = pika.PlainCredentials('user', 'password')
CONNECTION_PARAMS = pika.ConnectionParameters(host='rabbitmq', credentials=CREDENTIALS)

def main():
    connection = None
    # Bucle para intentar la conexión hasta que RabbitMQ esté listo
    while not connection:
        try:
            connection = pika.BlockingConnection(CONNECTION_PARAMS)
            print("[✅] Conexión con RabbitMQ establecida con éxito.")
        except pika.exceptions.AMQPConnectionError as e:
            print(f"[❌] No se pudo conectar a RabbitMQ ({e}). Reintentando en 5 segundos...")
            time.sleep(5)

    channel = connection.channel()
    channel.queue_declare(queue='booking_notifications', durable=True)

    def callback(ch, method, properties, body):
        message = json.loads(body)
        print(f"\n[📨] Notificación Recibida: {message}")
        print(f"    -> Enviando email de confirmación para la reserva #{message.get('id')}...")
        time.sleep(2)
        print(f"    -> Email enviado.")
        ch.basic_ack(delivery_tag=method.delivery_tag)

    channel.basic_consume(queue='booking_notifications', on_message_callback=callback)

    print('\n[*] El Servicio de Notificaciones está listo y esperando mensajes. Para salir presiona CTRL+C')
    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        print('Interrumpido')
        connection.close()

if __name__ == '__main__':
    main()