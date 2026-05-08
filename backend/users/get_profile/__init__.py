import azure.functions as func
from shared.db import get_container
from shared.auth import get_token_from_header
from shared.utils import success_response, error_response

def main(req: func.HttpRequest) -> func.HttpResponse:
    try:
        payload = get_token_from_header(req)
    except Exception as e:
        return error_response(str(e), 401)

    user_id = payload["sub"]
    container = get_container("users")

    try:
        user = container.read_item(item=user_id, partition_key=user_id)
    except Exception:
        return error_response("Usuario no encontrado", 404)

    return success_response({
        "id": user["id"],
        "email": user["email"],
        "username": user["username"],
        "role": user["role"],
        "avatar": user.get("avatar"),
        "bio": user.get("bio"),
        "created_at": user["created_at"],
        "preferences": user["preferences"]
    })