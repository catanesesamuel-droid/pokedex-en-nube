import azure.functions as func
from shared.db import get_container
from shared.auth import get_token_from_header
from shared.utils import success_response, error_response

VALID_ROLES = ["admin", "cliente"]

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
    new_role = body.get("role")

    if not target_id or not new_role:
        return error_response("user_id y role son obligatorios", 400)

    if new_role not in VALID_ROLES:
        return error_response(f"Rol inválido. Opciones: {VALID_ROLES}", 400)

    # No puede cambiarse el rol a sí mismo
    if target_id == payload["sub"]:
        return error_response("No puedes cambiar tu propio rol", 400)

    container = get_container("users")

    try:
        user = container.read_item(item=target_id, partition_key=target_id)
    except Exception:
        return error_response("Usuario no encontrado", 404)

    user["role"] = new_role
    container.replace_item(item=target_id, body=user)

    return success_response({
        "message": f"Rol actualizado correctamente",
        "user_id": target_id,
        "new_role": new_role
    })