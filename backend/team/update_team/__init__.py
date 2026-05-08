import azure.functions as func
from shared.db import get_container
from shared.auth import get_token_from_header
from shared.utils import success_response, error_response

VALID_FORMATS = ["singles", "doubles", "vgc", None]

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
    container = get_container("team")

    teams = list(container.query_items(
        query="SELECT * FROM c WHERE c.user_id = @user_id",
        parameters=[{"name": "@user_id", "value": user_id}],
        enable_cross_partition_query=True
    ))

    if not teams:
        return error_response("Equipo no encontrado", 404)

    team = teams[0]

    if "is_public" in body:
        if not isinstance(body["is_public"], bool):
            return error_response("is_public debe ser true o false", 400)
        team["is_public"] = body["is_public"]

    if "format" in body:
        if body["format"] not in VALID_FORMATS:
            return error_response(f"Formato inválido. Opciones: {VALID_FORMATS}", 400)
        team["format"] = body["format"]

    container.replace_item(item=team["id"], body=team)

    return success_response({"message": "Equipo actualizado correctamente", "team": team})