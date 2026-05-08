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
    container = get_container("favorites")

    favorites = list(container.query_items(
        query="SELECT * FROM c WHERE c.user_id = @user_id ORDER BY c.created_at DESC",
        parameters=[{"name": "@user_id", "value": user_id}],
        enable_cross_partition_query=True
    ))

    return success_response({"favorites": favorites, "total": len(favorites)})