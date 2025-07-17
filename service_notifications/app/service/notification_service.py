import time

class NotificationService:
    def handle_notification(self, message: dict):
        print(f"\n[📨] Notificación Recibida: {message}")
        print(f"    -> Enviando email de confirmación para la reserva #{message.get('id')}...")
        time.sleep(2)
        print(f"    -> Email enviado con éxito.")
