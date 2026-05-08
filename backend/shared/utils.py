import json
import azure.functions as func

def success_response(data: dict, status_code: int = 200) -> func.HttpResponse:
    return func.HttpResponse(
        body=json.dumps(data, ensure_ascii=False),
        status_code=status_code,
        mimetype="application/json"
    )

def error_response(message: str, status_code: int = 400) -> func.HttpResponse:
    return func.HttpResponse(
        body=json.dumps({"error": message}, ensure_ascii=False),
        status_code=status_code,
        mimetype="application/json"
    )