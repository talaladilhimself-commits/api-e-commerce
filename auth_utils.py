import jwt
from datetime import datetime, timedelta

SECRET_KEY = "veryverysecretkey"

def encode_jwt(payload):
    payload["exp"] = datetime.utcnow() + timedelta(hours=2) 
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

def decode_jwt(token):
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        return None  
    except jwt.InvalidTokenError:
        return None 
