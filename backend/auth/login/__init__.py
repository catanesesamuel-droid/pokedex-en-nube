import json
import bcrypt
import azure.functions as func
from shared.db import get_container
from shared.auth import generate_token
from shared.utils import success_response, error_response

def main(req: func.HttpRequest) -> func.HttpResponse:
    try:
        body = req.get_json()
    except ValueError:
        return error_response("Body inválido", 400)

    email = body.get("email", "").strip().lower()
    password = body.get("password", "")

    if not email or not password:
        return error_response("Email y password son obligatorios", 400)

    container = get_container("users")

    # Buscar usuario por email
    users = list(container.query_items(
        query="SELECT * FROM c WHERE c.email = @email",
        parameters=[{"name": "@email", "value": email}],
        enable_cross_partition_query=True
    ))

    if not users:
        return error_response("Credenciales incorrectas", 401)

    user = users[0]

    if not user.get("is_active"):
        return error_response("Cuenta bloqueada, contacta con un administrador", 403)

    # Verificar contraseña
    if not bcrypt.checkpw(password.encode("utf-8"), user["password_hash"].encode("utf-8")):
        return error_response("Credenciales incorrectas", 401)

    token = generate_token(user["id"], user["role"])

    return success_response({
        "message": "Login correcto",
        "token": token,
        "user": {
            "id": user["id"],
            "username": user["username"],
            "email": user["email"],
            "role": user["role"],
            "preferences": user["preferences"]
        }
    })