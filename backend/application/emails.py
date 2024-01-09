from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string


def send_invitation_email(email, url):
    plaintext = render_to_string(
        "invite_user_email.txt",
        {
            "email": email,
            "url": url,
        },
    )
    html_text = render_to_string(
        "invite_user_email.html",
        {
            "email": email,
            "url": url,
        },
    )

    msg = EmailMultiAlternatives(
        subject="アカウント登録のお知らせ",
        body=plaintext,
        from_email=None,
        to=[email],
        alternatives=[(html_text, "text/html")],
    )

    # 送信
    msg.send()


def send_reset_email(email, url):
    plaintext = render_to_string(
        "reset_password_email.txt",
        {
            "email": email,
            "url": url,
        },
    )
    html_text = render_to_string(
        "reset_password_email.html",
        {
            "email": email,
            "url": url,
        },
    )
    msg = EmailMultiAlternatives(
        subject="パスワード再設定のお知らせ",
        body=plaintext,
        from_email=None,
        to=[email],
        alternatives=[(html_text, "text/html")],
    )

    # 送信
    msg.send()
