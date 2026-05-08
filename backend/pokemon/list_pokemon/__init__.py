import requests
import azure.functions as func
from shared.auth import get_token_from_header
from shared.utils import success_response, error_response

def main(req: func.HttpRequest) -> func.HttpResponse:
    try:
        get_token_from_header(req)
    except Exception as e:
        return error_response(str(e), 401)

    limit = int(req.params.get("limit", 20))
    offset = int(req.params.get("offset", 0))

    response = requests.get(f"https://pokeapi.co/api/v2/pokemon?limit={limit}&offset={offset}")
    if response.status_code != 200:
        return error_response("Error al conectar con PokeAPI", 502)

    return success_response(response.json())