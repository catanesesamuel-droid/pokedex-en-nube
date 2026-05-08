# PokéDex Cloud - Documentación Técnica del Backend

## 🏗️ Arquitectura del Sistema
El backend está diseñado bajo un modelo **Serverless** utilizando **Azure Functions** con el modelo de programación de Python v2. Esta arquitectura permite una ejecución desacoplada, escalable y eficiente en costes.

### Componentes Principales:
- **Function App:** El contenedor principal que aloja todos los puntos de entrada (triggers HTTP).
- **Módulos de Función:** Cada funcionalidad principal está organizada en subcarpetas (auth, users, pokemon, favorites, team, admin) con su propia lógica.
- **Capa Compartida (`shared/`):** Contiene lógica reutilizable para la conexión a base de datos, autenticación JWT y utilidades de respuesta.

## 💾 Persistencia de Datos
Se utiliza **Azure Cosmos DB** (API SQL) como base de datos NoSQL. Los datos se organizan en los siguientes contenedores:

| Contenedor | Partition Key | Descripción |
|------------|---------------|-------------|
| `users` | `/id` | Información de cuentas, roles y perfiles. |
| `favorites` | `/id` | Relación de pokémons favoritos por usuario. |
| `team` | `/id` | Configuración de equipos Pokémon de los usuarios. |
| `reports` | `/id` | Datos de actividad y reportes del sistema. |

## 🔐 Seguridad y Autenticación
- **JWT (JSON Web Tokens):** Se generan tokens firmados tras un inicio de sesión exitoso. El backend valida la firma y la expiración en cada petición protegida.
- **Middleware de Autenticación:** La función `get_token_from_header` en `shared/auth.py` centraliza la extracción y validación de la identidad del usuario.
- **Autorización por Roles:** Ciertos endpoints (bajo la ruta `/mgmt/`) verifican que el claim `role` en el JWT sea `admin`.

## 📡 API Reference (Resumen de Rutas)

### Autenticación (`/auth`)
- `POST /register`: Crea un nuevo usuario en Cosmos DB.
- `POST /login`: Valida credenciales y devuelve un JWT.

### Usuarios (`/users`)
- `GET /profile`: Recupera los datos del usuario actual.
- `PUT /profile`: Actualiza username, bio y avatar.
- `PUT /preferences`: Guarda preferencias como el tema (dark/light).

### Pokémon (`/pokemon`)
- `GET /search`: Endpoint para búsqueda avanzada (parámetro `q`).
- `GET /{name_or_id}`: Obtiene detalles de un pokémon específico.

### Colecciones
- **Favoritos (`/favorites`):** `GET` (listar), `POST` (añadir), `DELETE` (eliminar).
- **Equipo (`/team`):** `GET` (ver), `POST` (añadir), `PUT` (actualizar formato/privacidad), `DELETE` (quitar).

### Administración (`/mgmt`)
- `GET /users`: Listado global de usuarios.
- `PUT /block`: Bloqueo/desbloqueo de cuentas.
- `PUT /role`: Cambio de permisos (User/Admin).

## ⚙️ Configuración y Variables de Entorno
El sistema requiere las siguientes variables configuradas en el entorno de ejecución (o `local.settings.json` para desarrollo):
- `COSMOS_ENDPOINT`: URL de la instancia de Cosmos DB.
- `COSMOS_KEY`: Clave primaria de acceso.
- `COSMOS_DATABASE`: Nombre de la base de datos (ej. `pokedex`).
- `JWT_SECRET`: Clave secreta para la firma de tokens.

## 🚀 Requisitos de Desarrollo
- Python 3.10 o superior.
- Azure Functions Core Tools.
- Dependencias listadas en `requirements.txt` (azure-functions, azure-cosmos, pyjwt, etc.).
