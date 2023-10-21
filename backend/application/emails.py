from django.core import mail
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

# def send_welcome_email(email):
#     plaintext = render_to_string("../templates/welcome_email.txt")
#     html_text = render_to_string("../templates/welcome_email.html")

#     mail.send_mail(
#         subject="ようこそ",
#         message=plaintext,
#         from_email="example@mail.com",
#         recipient_list=[email],
#         html_message=html_text,
#     )

def send_welcome_email(email, name, url):
    plaintext = render_to_string(
        "send_remind_email.txt",
        {
            "name": name,
            "email": email,
            "url": url,
        },
    )

    msg = EmailMultiAlternatives(
        subject="IDLink登録中メールアドレスのお知らせ",
        body=plaintext,
        from_email=None,
        to=[email],
    )

    # 送信
    msg.send()