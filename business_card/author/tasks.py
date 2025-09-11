import time, requests
from django.conf import settings
from django.core.mail import EmailMessage
from django.core.files.storage import default_storage
from django.template.loader import render_to_string

from celery import shared_task


def send_telegram(message:str, file_info:dict=None):
    """Sends a message to tg via bot."""
    data = {
        "chat_id": settings.TELEGRAM_USER_ID,
    }

    if file_info:
        data["caption"] = message
        requests.post(f"{settings.TELEGRAM_API_URL}sendDocument", data=data, files={"document": (file_info.get("name", "File"), file_info["file"])})
        return "Message with file on tg sent"

    data["text"] = message
    requests.post(f"{settings.TELEGRAM_API_URL}sendMessage", json=data)
    return "Message sent to tg"
    

def send_email(message:str, file_info:dict=None):
    """Sends an email to the specified email address if the specified file path appends a file to the email."""

    email = EmailMessage(
        subject="Messages from business card sites",
        body=render_to_string("email_templates/email.html", context={"message": message }),
        from_email=None,
        to=settings.EMAIL_RECIPIENT,
    )

    email.content_subtype = "html"

    if file_info:
        email.attach(file_info.get("name", "File"), file_info["file"])

    email.send(fail_silently=False)
    return "Email sent"


@shared_task
def send_messange_task(message:str, file_path:str):
    """Performs two functions: send_telegram and send_email."""

    if file_path:
        time.sleep(1)
        with default_storage.open(file_path, "rb") as file:
            file_info = {
                "name": file_path.split("/")[-1], 
                "file": file.read(),
            }
        print(send_telegram(message,file_info))
        print(send_email(message, file_info))

        default_storage.delete(file_path)
        return "Message sent with file"

    print(send_telegram(message))
    print(send_email(message))
    return "Message sent"