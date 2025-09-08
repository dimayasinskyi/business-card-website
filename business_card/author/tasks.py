import time
from django.core.mail import EmailMessage
from django.core.files.storage import default_storage

from celery import shared_task


@shared_task
def send_email_task(subject:str, message:str, email:list, file_path:str):
    """Sends an email to the specified email address if the specified file path appends a file to the email."""
    email = EmailMessage(
        subject=subject,
        body=message,
        from_email=None,
        to=email,
    )

    if file_path:
        time.sleep(1)
        with default_storage.open(file_path, "rb") as file:
            email.attach(file_path.split("/")[-1], file.read())
        default_storage.delete(file_path)

    email.send(fail_silently=False)
    return "Email message sent"