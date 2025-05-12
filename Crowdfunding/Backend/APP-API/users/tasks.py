from django.core.mail import send_mail
from django.conf import settings
from django_rq import job

@job
def send_welcome_email(user_email):
    subject = 'Bienvenido a CrowdFundMe'
    message = 'Gracias por registrarte en CrowdFundMe. Estamos emocionados de tenerte con nosotros.'
    from_email = settings.DEFAULT_FROM_EMAIL

    send_mail(subject, message, from_email, [user_email])