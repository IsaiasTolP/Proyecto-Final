from django.core.mail import send_mail
from django.conf import settings
from django_rq import job
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.contrib.auth.models import User

@job
def send_welcome_email(user_email):
    subject = 'Bienvenido a CrowdFundMe'
    message = 'Gracias por registrarte en CrowdFundMe. Estamos emocionados de tenerte con nosotros.'
    from_email = settings.DEFAULT_FROM_EMAIL

    send_mail(subject, message, from_email, [user_email])

@job
def send_recover_email(user_email, user: User):
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)
    reset_url = f'{settings.FRONTEND_URL}/reset-password?uid={uid}&token={token}'

    send_mail(
        subject='Recupera tu contraseña',
        message=f'Haz click en el siguiente enlace para restablecer tu contraseña:\n{reset_url}',
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user_email],
        fail_silently=False,
    )