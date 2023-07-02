from django.core import mail
from django.template.loader import render_to_string


def send_welcome_email(email):
    plaintext = render_to_string("../templates/welcome_email.txt")
    html_text = render_to_string("../templates/welcome_email.html")

    mail.send_mail(
        subject="ようこそ",
        message=plaintext,
        from_email="example@mail.com",
        recipient_list=[email],
        html_message=html_text,
    )
