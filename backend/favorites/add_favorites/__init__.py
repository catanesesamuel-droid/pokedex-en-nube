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
    container = get_container("favorites")

    # Comprobar si ya está en favoritos
    existing = list(container.query_items(
        query="SELECT * FROM c WHERE c.user_id = @user_id AND c.pokemon_id = @pokemon_id",
        parameters=[
            {"name": "@user_id", "value": user_id},
            {"name": "@pokemon_id", "value": int(pokemon_id)}
        ],
        enable_cross_partition_query=True
    ))
    if existing:
        return error_response("El pokemon ya está en favoritos", 409)

    favorite = {
        "id": str(uuid.uuid4()),
        "user_id": user_id,
        "pokemon_id": pokemon_id,
        "pokemon_name": pokemon_name,
        "created_at": datetime.utcnow().isoformat()
    }

    container.create_item(favorite)

    return success_response({"message": "Pokemon añadido a favoritos", "favorite": favorite}, 201)