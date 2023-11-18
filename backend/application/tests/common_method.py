def mail_confirm(mail_outbox, sender: str, message: str):
    """メールが正常に送信されたかどうかを確認するテスト
    Args:
        mail_outbox (List[EmailMessage]): Djangoテスト用のメールの受信ボックス
        sender (str): メールの送り主
        message (str): メールの件名
    """
    # メールを1通受信したことを確認
    assert len(mail_outbox) == 1
    assert mail_outbox[0].subject == message
    assert mail_outbox[0].from_email == "webmaster@localhost"
    assert mail_outbox[0].to[0] == sender
