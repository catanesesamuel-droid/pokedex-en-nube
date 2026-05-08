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

    container = get_container("users")

    users = list(container.query_items(
        query="SELECT c.id, c.email, c.username, c.role, c.is_active, c.created_at FROM c",
        enable_cross_partition_query=True
    ))

    return success_response({"users": users, "total": len(users)})