from django.core import mail
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string


def send_invitation_email(email, name, url):
    plaintext = render_to_string(
        "invite_user_email.txt",
        {
            "name": name,
            "email": email,
            "url": url,
        },
    )

    msg = EmailMultiAlternatives(
        subject="アカウント登録のお知らせ",
        body=plaintext,
        from_email=None,
        to=[email],
    )

    # 送信
    msg.send()