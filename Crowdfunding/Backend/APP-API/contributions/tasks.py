from django.core.mail import EmailMessage, send_mail
from django.template.loader import render_to_string
from weasyprint import HTML
import tempfile
from django.conf import settings
from django_rq import job

@job
def send_receipt_email(user_email, project_name, amount):
    subject = 'Gracias por tu contribución a {}'.format(project_name)
    from_email = settings.DEFAULT_FROM_EMAIL
    to_email = user_email

    html_string = render_to_string('templates/emails/receipt.html', {
        'project_name': project_name,
        'amount': amount,
        'user_email': user_email,
    })

    with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as output:
        HTML(string=html_string).write_pdf(output)
        pdf_file = output.name
    output.close()

    email = EmailMessage(
        subject,
        body = 'Has contribuido con {} a {}. ¡Gracias por tu apoyo!'.format(amount, project_name),
        from_email=from_email,
        to=to_email,
    )
    
    email.attach_file('receipt.pdf', open(pdf_file, 'rb').read(), 'application/pdf')
    email.send()

@job
def send_received_contribution_email(user_email, project_name, amount):
    subject = 'Contribución recibida para {}'.format(project_name)
    message = 'Has recibido una contribución de {} para el proyecto {}. ¡Gracias por confiar en nosotros para su proyecto!'.format(amount, project_name)
    from_email = settings.DEFAULT_FROM_EMAIL

    send_mail(subject, message, from_email, [user_email])