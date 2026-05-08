# 📚 Guía de Integración - PokéDex Cloud

## 🚀 Setup del Frontend

### 1. Configurar la URL de la API

En `index.html`, línea ~730, cambia:
```javascript
const API_BASE = 'https://your-functions-app.azurewebsites.net/api';
```
Por la URL de tu Azure Functions App. La encuentras en Azure Portal → Function App → URL.

### 2. Configurar CORS en Azure Functions

En `host.json` añade configuración CORS:
```json
{
  "version": "2.0",
  "extensions": {
    "http": {
      "routePrefix": "api",
      "cors": {
        "allowedOrigins": ["*"],
        "allowedMethods": ["GET","POST","PUT","DELETE","OPTIONS"],
        "allowedHeaders": ["*"]
      }
    }
  }
}
```

O configúralo desde Azure Portal → Function App → CORS → Añadir `*` (en producción usa tu dominio).

### 3. Deploy del Frontend

Opciones en Azure:
- **Azure Static Web Apps** (recomendado, gratis): Sube `index.html` al repo y conecta con GitHub Actions
- **Azure Blob Storage** con Static Website habilitado
- **Azure CDN** sobre el Blob Storage

---

## ⚠️ Gaps en el Backend detectados

### 1. `add_favorites/__init__.py` — Bug crítico

El archivo `add_favorites/__init__.py` tiene el código de **GET** en lugar de **POST**:

```python
# CÓDIGO ACTUAL (incorrecto - es igual que get_favorites)
def main(req: func.HttpRequest) -> func.HttpResponse:
    user_id = payload["sub"]
    favorites = list(container.query_items(...))
    return success_response({"favorites": favorites, ...})
```

**FIX necesario:**
```python
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

    # Verificar que no esté ya en favoritos
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

    fav = {
        "id": str(uuid.uuid4()),
        "user_id": user_id,
        "pokemon_id": int(pokemon_id),
        "pokemon_name": pokemon_name,
        "created_at": datetime.utcnow().isoformat()
    }
    container.create_item(fav)
    return success_response({"message": "Pokemon añadido a favoritos", "favorite": fav}, 201)
```

### 2. Falta endpoint `GET /pokemon/search` (lista general)

El `search_pokemon` actual requiere un `name_or_id` en la ruta, pero falta un endpoint para listar pokémons con paginación. El frontend lo suple consumiendo PokeAPI directamente, pero si quieres cachear en backend, añade:

```python
# backend/pokemon/list_pokemon/__init__.py
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
```

### 3. Falta contenedor `reports` en CosmosDB

El endpoint `GET /admin/reports` consulta un contenedor `reports` que no está en el schema. Créalo en CosmosDB con partition key `/id`.

### 4. Contenedores CosmosDB necesarios

Asegúrate de crear todos estos en tu base de datos `pokedex`:

| Contenedor  | Partition Key |
|-------------|---------------|
| `users`     | `/id`         |
| `favorites` | `/id`         |
| `team`      | `/id`         |
| `reports`   | `/id`         |

### 5. Variables de entorno en Azure Functions

En Azure Portal → Function App → Configuration → Application Settings:
```
COSMOS_ENDPOINT   = https://tu-cosmos.documents.azure.com:443/
COSMOS_KEY        = tu-clave-primaria
COSMOS_DATABASE   = pokedex
JWT_SECRET        = clave-larga-aleatoria-minimo-32-chars
```

---

## 🏗️ Infraestructura Terraform pendiente

El `main.tf` actual solo crea el Resource Group. Añade estos recursos:

```hcl
# Cosmos DB
resource "azurerm_cosmosdb_account" "main" {
  name                = "cosmos-pokedex"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
  offer_type          = "Standard"
  kind                = "GlobalDocumentDB"
  consistency_policy { consistency_level = "Session" }
  geo_location { location = azurerm_resource_group.main.location; failover_priority = 0 }
}

resource "azurerm_cosmosdb_sql_database" "main" {
  name                = "pokedex"
  resource_group_name = azurerm_resource_group.main.name
  account_name        = azurerm_cosmosdb_account.main.name
}

# Storage Account (para Functions)
resource "azurerm_storage_account" "main" {
  name                     = "stpokedex"
  resource_group_name      = azurerm_resource_group.main.name
  location                 = azurerm_resource_group.main.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
}

# Function App
resource "azurerm_service_plan" "main" {
  name                = "asp-pokedex"
  resource_group_name = azurerm_resource_group.main.name
  location            = azurerm_resource_group.main.location
  os_type             = "Linux"
  sku_name            = "Y1"  # Consumption plan (gratis)
}

resource "azurerm_linux_function_app" "main" {
  name                = "func-pokedex"
  resource_group_name = azurerm_resource_group.main.name
  location            = azurerm_resource_group.main.location
  storage_account_name       = azurerm_storage_account.main.name
  storage_account_access_key = azurerm_storage_account.main.primary_access_key
  service_plan_id            = azurerm_service_plan.main.id
  site_config {
    application_stack { python_version = "3.11" }
    cors { allowed_origins = ["*"] }
  }
  app_settings = {
    COSMOS_ENDPOINT  = azurerm_cosmosdb_account.main.endpoint
    COSMOS_KEY       = azurerm_cosmosdb_account.main.primary_key
    COSMOS_DATABASE  = "pokedex"
    JWT_SECRET       = "cambia-esto-por-una-clave-segura"
  }
}

# Static Web App (frontend)
resource "azurerm_static_web_app" "main" {
  name                = "swa-pokedex"
  resource_group_name = azurerm_resource_group.main.name
  location            = "westeurope"
  sku_tier            = "Free"
}
```

---

## 📋 Endpoints del Backend (resumen)

| Método | Ruta | Auth | Descripción |
|--------|------|------|-------------|
| POST | `/auth/register` | ❌ | Registrar usuario |
| POST | `/auth/login` | ❌ | Login → JWT |
| POST | `/auth/logout` | ✅ | Logout (client-side) |
| GET | `/users/profile` | ✅ | Ver perfil |
| PUT | `/users/profile` | ✅ | Editar perfil |
| PUT | `/users/preferences` | ✅ | Preferencias |
| DELETE | `/users/account` | ✅ | Eliminar cuenta |
| GET | `/pokemon/{name_or_id}` | ✅ | Info pokémon |
| GET | `/favorites` | ✅ | Listar favoritos |
| POST | `/favorites` | ✅ | Añadir favorito |
| DELETE | `/favorites/{pokemon_id}` | ✅ | Eliminar favorito |
| GET | `/team` | ✅ | Ver equipo |
| POST | `/team` | ✅ | Añadir al equipo |
| PUT | `/team` | ✅ | Actualizar equipo |
| DELETE | `/team/{pokemon_id}` | ✅ | Quitar del equipo |
| GET | `/admin/users` | 🛡️ admin | Listar usuarios |
| PUT | `/admin/users/block` | 🛡️ admin | Bloquear/Activar |
| PUT | `/admin/users/role` | 🛡️ admin | Cambiar rol |
| PUT | `/admin/users/reset-password` | 🛡️ admin | Reset password |
| GET | `/admin/reports` | 🛡️ admin | Ver reportes |
