import bcrypt
import azure.functions as func
from shared.db import get_container
from shared.auth import get_token_from_header
from shared.utils import success_response, error_response

def main(req: func.HttpRequest) -> func.HttpResponse:
    try:
        payload = get_token_from_header(req)
    except Exception as e:
        return error_response(str(e), 401)

    if payload["role"] != "admin":
        return error_response("Acceso denegado", 403)

    try:
        body = req.get_json()
    except ValueError:
        return error_response("Body inválido", 400)

    target_id = body.get("user_id")
    new_password = body.get("new_password")

    if not target_id or not new_password:
        return error_response("user_id y new_password son obligatorios", 400)

    if len(new_password) < 8:
        return error_response("La contraseña debe tener al menos 8 caracteres", 400)

    container = get_container("users")

    try:
        user = container.read_item(item=target_id, partition_key=target_id)
    except Exception:
        return error_response("Usuario no encontrado", 404)

    user["password_hash"] = bcrypt.hashpw(
        new_password.encode("utf-8"), bcrypt.gensalt()
    ).decode("utf-8")

    container.replace_item(item=target_id, body=user)

    return success_response({"message": "Contraseña actualizada correctamente"})