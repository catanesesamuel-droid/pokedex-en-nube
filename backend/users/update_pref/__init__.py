import azure.functions as func
from shared.db import get_container
from shared.auth import get_token_from_header
from shared.utils import success_response, error_response

VALID_THEMES = ["light", "dark"]
VALID_LANGUAGES = ["es", "en"]
VALID_PRIVACY = ["public", "private"]

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
    container = get_container("users")

    try:
        user = container.read_item(item=user_id, partition_key=user_id)
    except Exception:
        return error_response("Usuario no encontrado", 404)

    prefs = user.get("preferences", {})

    if "theme" in body:
        if body["theme"] not in VALID_THEMES:
            return error_response(f"Tema inválido. Opciones: {VALID_THEMES}", 400)
        prefs["theme"] = body["theme"]

    if "language" in body:
        if body["language"] not in VALID_LANGUAGES:
            return error_response(f"Idioma inválido. Opciones: {VALID_LANGUAGES}", 400)
        prefs["language"] = body["language"]

    if "privacy" in body:
        if body["privacy"] not in VALID_PRIVACY:
            return error_response(f"Privacidad inválida. Opciones: {VALID_PRIVACY}", 400)
        prefs["privacy"] = body["privacy"]

    user["preferences"] = prefs
    container.replace_item(item=user_id, body=user)

    return success_response({
        "message": "Preferencias actualizadas correctamente",
        "preferences": prefs
    })