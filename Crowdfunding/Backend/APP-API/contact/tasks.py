# contact/tasks.py
from django.core.mail import send_mail
from django.conf import settings

def send_contact_email(name: str, email: str, message: str):
    subject = f"Nuevo mensaje de contacto de {name}"
    body = f"Nombre: {name}\nCorreo: {email}\n\nMensaje:\n{message}"
    send_mail(
        subject,
        body,
        settings.DEFAULT_FROM_EMAIL,
        [settings.DEFAULT_FROM_EMAIL], 
        fail_silently=False,
    )
