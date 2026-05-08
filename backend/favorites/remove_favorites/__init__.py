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
    container = get_container("favorites")

    existing = list(container.query_items(
        query="SELECT * FROM c WHERE c.user_id = @user_id AND c.pokemon_id = @pokemon_id",
        parameters=[
            {"name": "@user_id", "value": user_id},
            {"name": "@pokemon_id", "value": int(pokemon_id)}
        ],
        enable_cross_partition_query=True
    ))

    if not existing:
        return error_response("El pokemon no está en favoritos", 404)

    fav = existing[0]
    container.delete_item(item=fav["id"], partition_key=fav["id"])

    return success_response({"message": "Pokemon eliminado de favoritos"})