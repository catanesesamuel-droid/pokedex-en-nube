import azure.functions as func
from shared.auth import get_token_from_header
from shared.utils import success_response, error_response

def main(req: func.HttpRequest) -> func.HttpResponse:
    try:
        get_token_from_header(req)
    except Exception as e:
        return error_response(str(e), 401)

    # JWT es stateless, el logout lo gestiona el cliente eliminando el token
    return success_response({"message": "Sesión cerrada correctamente"})