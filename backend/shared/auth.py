import jwt
import os
from datetime import datetime, timedelta

def generate_token(user_id: str, role: str) -> str:
    payload = {
        "sub": user_id,
        "role": role,
        "exp": datetime.utcnow() + timedelta(hours=24)
    }
    return jwt.encode(payload, os.environ["JWT_SECRET"], algorithm="HS256")

def validate_token(token: str) -> dict:
    try:
        return jwt.decode(token, os.environ["JWT_SECRET"], algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        raise Exception("Token expirado")
    except jwt.InvalidTokenError:
        raise Exception("Token inválido")

def get_token_from_header(req) -> dict:
    auth_header = req.headers.get("Authorization", "")
    if not auth_header.startswith("Bearer "):
        raise Exception("Token no proporcionado")
    token = auth_header.split(" ")[1]
    return validate_token(token)