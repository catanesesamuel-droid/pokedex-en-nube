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

    container = get_container("reports")

    reports = list(container.query_items(
        query="SELECT * FROM c ORDER BY c.created_at DESC",
        enable_cross_partition_query=True
    ))

    return success_response({"reports": reports, "total": len(reports)})