import uuid
import azure.functions as func
from datetime import datetime
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

    pokemon_id = body.get("pokemon_id")
    pokemon_name = body.get("pokemon_name")

    if not pokemon_id or not pokemon_name:
        return error_response("pokemon_id y pokemon_name son obligatorios", 400)

    user_id = payload["sub"]
    container = get_container("team")

    teams = list(container.query_items(
        query="SELECT * FROM c WHERE c.user_id = @user_id",
        parameters=[{"name": "@user_id", "value": user_id}],
        enable_cross_partition_query=True
    ))

    if teams:
        team = teams[0]
        if len(team["slots"]) >= 6:
            return error_response("El equipo ya tiene 6 pokémons", 400)

        # Comprobar si ya está en el equipo
        if any(s["pokemon_id"] == pokemon_id for s in team["slots"]):
            return error_response("El pokemon ya está en el equipo", 409)

        team["slots"].append({
            "pokemon_id": pokemon_id,
            "pokemon_name": pokemon_name
        })
        container.replace_item(item=team["id"], body=team)
    else:
        team = {
            "id": str(uuid.uuid4()),
            "user_id": user_id,
            "slots": [{"pokemon_id": pokemon_id, "pokemon_name": pokemon_name}],
            "format": None,
            "is_public": False,
            "created_at": datetime.utcnow().isoformat()
        }
        container.create_item(team)

    return success_response({"message": "Pokemon añadido al equipo", "team": team}, 201)