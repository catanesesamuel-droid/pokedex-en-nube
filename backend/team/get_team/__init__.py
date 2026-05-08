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
    container = get_container("team")

    teams = list(container.query_items(
        query="SELECT * FROM c WHERE c.user_id = @user_id",
        parameters=[{"name": "@user_id", "value": user_id}],
        enable_cross_partition_query=True
    ))

    team = teams[0] if teams else {"slots": [], "is_public": False, "format": None}

    return success_response({"team": team})