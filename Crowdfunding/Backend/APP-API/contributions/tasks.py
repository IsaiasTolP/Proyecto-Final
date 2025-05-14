import os
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from weasyprint import HTML
import tempfile
from django.conf import settings
from django_rq import job
import uuid
import datetime

BASE_URL = settings.STATIC_ROOT or os.path.join(settings.BASE_DIR, 'static')

@job
def send_receipt_email(user_email, user_name, project_name, amount):
    subject = 'Gracias por tu contribución a {}'.format(project_name)
    from_email = settings.DEFAULT_FROM_EMAIL
    to_email = user_email
    invoice_number = uuid.uuid4()

    html_string = render_to_string('emails/receipt.html', {
        'project_name': project_name,
        'amount': amount,
        'user_email': user_email,
        'user_name': user_name,
        'invoice_number':invoice_number,
        'issue_date': datetime.date.today(),
    })


    with tempfile.NamedTemporaryFile(delete=False, prefix=f'Factura {invoice_number}', suffix='.pdf') as output:
        HTML(string=html_string, base_url=BASE_URL).write_pdf(output)
        pdf_file = output.name
    output.close()

    email = EmailMessage(
        subject,
        body = 'Has contribuido con {} € a {}. ¡Gracias por tu apoyo!'.format(amount, project_name),
        from_email=from_email,
        to=[to_email],
    )
    content = open(pdf_file, 'rb').read()
    
    email.attach(pdf_file, content, 'application/pdf')
    email.send()

@job
def send_received_contribution_email(user_email, project_name, amount):
    subject = 'Contribución recibida para {}'.format(project_name)
    message = 'Has recibido una contribución de {} para el proyecto {}. ¡Gracias por confiar en nosotros para su proyecto!'.format(amount, project_name)
    from_email = settings.DEFAULT_FROM_EMAIL
    to_email = user_email
    invoice_number = uuid.uuid4()

    html_string = render_to_string('emails/owner_receipt.html', {
        'project_name': project_name,
        'amount': amount,
        'invoice_number': invoice_number,
        'issue_date': datetime.date.today(),
    })

    with tempfile.NamedTemporaryFile(delete=False, prefix=f'Recibo {invoice_number}', suffix='.pdf') as output:
        HTML(string=html_string, base_url=BASE_URL).write_pdf(output)
        pdf_file = output.name
    output.close()

    email = EmailMessage(
        subject,
        body = message,
        from_email=from_email,
        to=[to_email],
    )

    content = open(pdf_file, 'rb').read()
    
    email.attach(pdf_file, content, 'application/pdf')
    email.send()