import json
import uuid
import bcrypt
import azure.functions as func
from datetime import datetime
from shared.db import get_container
from shared.utils import success_response, error_response

def main(req: func.HttpRequest) -> func.HttpResponse:
    try:
        body = req.get_json()
    except ValueError:
        return error_response("Body inválido", 400)

    email = body.get("email", "").strip().lower()
    username = body.get("username", "").strip()
    password = body.get("password", "")

    if not email or not username or not password:
        return error_response("Email, username y password son obligatorios", 400)

    if len(password) < 8:
        return error_response("La contraseña debe tener al menos 8 caracteres", 400)

    container = get_container("users")

    # Comprobar si el email ya existe
    existing = list(container.query_items(
        query="SELECT * FROM c WHERE c.email = @email",
        parameters=[{"name": "@email", "value": email}],
        enable_cross_partition_query=True
    ))
    if existing:
        return error_response("El email ya está registrado", 409)

    # Comprobar si el username ya existe
    existing_username = list(container.query_items(
        query="SELECT * FROM c WHERE c.username = @username",
        parameters=[{"name": "@username", "value": username}],
        enable_cross_partition_query=True
    ))
    if existing_username:
        return error_response("El username ya está en uso", 409)

    # Hashear contraseña
    password_hash = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

    user = {
        "id": str(uuid.uuid4()),
        "email": email,
        "username": username,
        "password_hash": password_hash,
        "role": "cliente",
        "avatar": None,
        "bio": None,
        "created_at": datetime.utcnow().isoformat(),
        "is_active": True,
        "preferences": {
            "theme": "light",
            "language": "es",
            "privacy": "public"
        }
    }

    container.create_item(user)

    return success_response({
        "message": "Usuario registrado correctamente",
        "user_id": user["id"],
        "username": user["username"]
    }, 201)