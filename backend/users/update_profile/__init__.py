import azure.functions as func
from shared.db import get_container
from shared.auth import get_token_from_header
from shared.utils import success_response, error_response

def main(req: func.HttpRequest) -> func.HttpResponse:
    try:
        payload = get_token_from_header(req)
    except Exception as e:
        return error_response(str(e), 401)

    try:
        body = req.get_json()
    except ValueError:
        return error_response("Body inválido", 400)

    user_id = payload["sub"]
    container = get_container("users")

    try:
        user = container.read_item(item=user_id, partition_key=user_id)
    except Exception:
        return error_response("Usuario no encontrado", 404)

    # Solo se pueden actualizar avatar y bio
    if "avatar" in body:
        user["avatar"] = body["avatar"]
    if "bio" in body:
        user["bio"] = body["bio"]
    if "username" in body and body["username"].strip():
        # Comprobar que el username no esté en uso
        existing = list(container.query_items(
            query="SELECT * FROM c WHERE c.username = @username AND c.id != @id",
            parameters=[
                {"name": "@username", "value": body["username"].strip()},
                {"name": "@id", "value": user_id}
            ],
            enable_cross_partition_query=True
        ))
        if existing:
            return error_response("El username ya está en uso", 409)
        user["username"] = body["username"].strip()

    container.replace_item(item=user_id, body=user)

    return success_response({
        "message": "Perfil actualizado correctamente",
        "user": {
            "id": user["id"],
            "username": user["username"],
            "avatar": user.get("avatar"),
            "bio": user.get("bio")
        }
    })