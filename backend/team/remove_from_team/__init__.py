import azure.functions as func
from shared.db import get_container
from shared.auth import get_token_from_header
from shared.utils import success_response, error_response

def main(req: func.HttpRequest) -> func.HttpResponse:
    try:
        payload = get_token_from_header(req)
    except Exception as e:
        return error_response(str(e), 401)

    pokemon_id = req.route_params.get("pokemon_id")
    if not pokemon_id:
        return error_response("pokemon_id es obligatorio", 400)

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
    original_count = len(team["slots"])
    team["slots"] = [s for s in team["slots"] if str(s["pokemon_id"]) != str(pokemon_id)]

    if len(team["slots"]) == original_count:
        return error_response("El pokemon no está en el equipo", 404)

    container.replace_item(item=team["id"], body=team)

    return success_response({"message": "Pokemon eliminado del equipo", "team": team})