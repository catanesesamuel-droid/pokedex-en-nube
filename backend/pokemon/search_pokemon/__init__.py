import requests
import azure.functions as func
from shared.auth import get_token_from_header
from shared.utils import success_response, error_response

def main(req: func.HttpRequest) -> func.HttpResponse:
    try:
        get_token_from_header(req)
    except Exception as e:
        return error_response(str(e), 401)

    q = req.params.get("q", "").lower()
    if not q:
        return error_response("Se requiere el parámetro de búsqueda 'q'", 400)

    response = requests.get(f"https://pokeapi.co/api/v2/pokemon/{q}")
    if response.status_code == 404:
        return error_response("Pokemon no encontrado", 404)
    if response.status_code != 200:
        return error_response("Error al conectar con PokeAPI", 502)

    data = response.json()

    # Obtener información de especie para evoluciones y descripción
    species_response = requests.get(f"https://pokeapi.co/api/v2/pokemon-species/{name_or_id}")
    species_data = species_response.json() if species_response.status_code == 200 else {}

    pokemon = {
        "id": data["id"],
        "name": data["name"],
        "number": data["id"],
        "types": [t["type"]["name"] for t in data["types"]],
        "color": species_data.get("color", {}).get("name"),
        "region": species_data.get("generation", {}).get("name"),
        "stats": {
            "hp": data["stats"][0]["base_stat"],
            "attack": data["stats"][1]["base_stat"],
            "defense": data["stats"][2]["base_stat"],
            "special_attack": data["stats"][3]["base_stat"],
            "special_defense": data["stats"][4]["base_stat"],
            "speed": data["stats"][5]["base_stat"]
        },
        "attacks": [m["move"]["name"] for m in data["moves"][:10]],
        "images": {
            "sprite_normal": data["sprites"]["front_default"],
            "sprite_shiny": data["sprites"]["front_shiny"],
            "official_art": data["sprites"]["other"]["official-artwork"]["front_default"]
        },
        "evolution_chain_url": species_data.get("evolution_chain", {}).get("url")
    }

    return success_response(pokemon)