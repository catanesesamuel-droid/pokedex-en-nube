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
        container.read_item(item=user_id, partition_key=user_id)
    except Exception:
        return error_response("Usuario no encontrado", 404)

    # Eliminar favoritos del usuario
    favorites_container = get_container("favorites")
    favorites = list(favorites_container.query_items(
        query="SELECT * FROM c WHERE c.user_id = @user_id",
        parameters=[{"name": "@user_id", "value": user_id}],
        enable_cross_partition_query=True
    ))
    for fav in favorites:
        favorites_container.delete_item(item=fav["id"], partition_key=fav["id"])

    # Eliminar equipo del usuario
    team_container = get_container("team")
    teams = list(team_container.query_items(
        query="SELECT * FROM c WHERE c.user_id = @user_id",
        parameters=[{"name": "@user_id", "value": user_id}],
        enable_cross_partition_query=True
    ))
    for team in teams:
        team_container.delete_item(item=team["id"], partition_key=team["id"])

    # Eliminar usuario
    container.delete_item(item=user_id, partition_key=user_id)

    return success_response({"message": "Cuenta eliminada correctamente"})