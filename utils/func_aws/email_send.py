import smtplib
from email.mime.text import MIMEText
import base64
import json

import jwt


def handler(event, context):
    body_json = base64.b64decode(event['body']).decode('utf-8') if event['isBase64Encoded'] else event['body']
    body = json.loads(body_json)
    if token := event['headers'].get('Authorization'):
        data = jwt.decode(token, "YgQbzJ1PyQxIzlMeBKQs5o5IqOHJOVT9", algorithms=["HS256"])
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        sender = data.get('sender')
        password = data.get('password')
        msg = MIMEText(body.get('message'))
        subject = body.get('subject')
        recipient = body.get('recipient')
        if not sender or not password:
            return {
                "statusCode": 400,
                "body": "Sender and password are required! token: " + token + "не валидный"
            }
        try:
            server.login(sender, password)
            msg["Subject"] = subject
            server.sendmail(sender, recipient, msg.as_string())

            return {
                "statusCode": 200,
                "body": "The message was sent successfully!"
            }
        except Exception as _ex2:
            return {
                "statusCode": 400,
                "body": f"Error: {_ex2}"
            }
    else:
        return {
            "statusCode": 401,
            "headers": "Token is required!"
        }

# todo чтобы отправить сообщение по gmail адресу нужно включить доступ к "ненадежным приложениям" по ссылке:
# https://myaccount.google.com/u/0/lesssecureapps.
