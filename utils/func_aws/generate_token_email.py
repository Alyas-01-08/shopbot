import base64
import json
from json import JSONDecodeError

import jwt


def handler(event, context):
    body_json = base64.b64decode(event['body']).decode('utf-8') if event['isBase64Encoded'] else event['body']
    try:
        body = json.loads(body_json)
    except JSONDecodeError as _ex:
        return {
            "statusCode": 400,
            "body": f"Error: {_ex}"
        }
    sender = body.get('sender')
    password = body.get('password')
    smtp = body.get('smtp')
    if not sender or not password:
        return {
            "statusCode": 400,
            "body": "Sender and password are required!"
        }
    if not smtp:
        smtp = "smtp.gmail.com"
    port = body.get('port')
    if not port:
        port = 587
    encoded_jwt = jwt.encode(body.update(smtp=smtp, port=port), "YgQbzJ1PyQxIzlMeBKQs5o5IqOHJOVT9",
                             algorithm="HS256")
    return {'token': encoded_jwt}
