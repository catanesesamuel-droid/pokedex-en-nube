# Especificación Técnica de Infraestructura (Deep Dive)

## 1. Stack Tecnológico de IaC
*   **Herramienta:** Terraform v1.x
*   **Proveedor:** `azurerm` (Azure Resource Manager) ~> 3.90
*   **Estado (State):** Almacenado de forma remota en un Blob Storage de Azure (`tfstate-rg`) para permitir la automatización mediante pipelines de CI/CD (GitHub Actions).

## 2. Topología de Recursos

### 2.1. Gestión de Identidad y Acceso (IAM)
El diseño implementa el principio de **Mínimo Privilegio**:
*   **Managed Identity (System Assigned):** La `azurerm_linux_function_app` tiene habilitada una identidad propia en Azure AD.
*   **Key Vault Access Policy:** Se otorga permiso específico (`Get`, `List`) a la identidad de la función sobre los secretos del Key Vault, eliminando la necesidad de manejar credenciales manuales.

### 2.2. Capa de Datos: Cosmos DB
*   **Modelo de consistencia:** `Session` (Equilibrio óptimo entre rendimiento y consistencia de datos para aplicaciones web).
*   **Particionado:** Todos los contenedores (`users`, `favorites`, `reports`, `team`) utilizan `/id` como clave de partición para optimizar las consultas puntuales.
*   **Kind:** `GlobalDocumentDB` (SQL API).

### 2.3. Capa de Cómputo: Azure Functions
*   **Runtime:** Python 3.11 sobre Linux.
*   **Hosting Plan:** `Y1` Consumption Plan (Serverless).
*   **Configuración Crítica:**
    *   `EnableWorkerIndexing`: Habilitado para soportar el nuevo modelo de programación de Python en Azure Functions.
    *   `CORS`: Actualmente configurado en `*` para el entorno universitario, pendiente de restricción a la URL del Storage Account.

### 2.4. Seguridad de Secretos
Los secretos no se exponen en las variables de entorno como texto plano. Se utiliza la sintaxis de referencia de Key Vault:
```hcl
COSMOS_KEY = "@Microsoft.KeyVault(SecretUri=${azurerm_key_vault_secret.cosmos_key.id})"
JWT_SECRET = "@Microsoft.KeyVault(SecretUri=${azurerm_key_vault_secret.jwt_secret.id})"
```
Esto asegura que el valor solo se resuelva en tiempo de ejecución dentro de la memoria de la función.

## 3. Almacenamiento y Frontend
*   **Static Website:** Se utiliza el servicio de `$web` integrado en el Storage Account.
*   **Index/Error:** Configurados `index.html` y `error.html` para el manejo de rutas en el lado del cliente (SPA).

## 4. Observabilidad
*   **Application Insights:** Vinculado a la Function App para capturar trazas de ejecución de Python, excepciones y métricas de rendimiento de las peticiones HTTP.
*   **Log Analytics Workspace:** Repositorio central de logs con una retención configurada de 30 días para auditoría.

## 5. Variables y Parámetros
*   `jwt_secret`: Única variable de entrada marcada como `sensitive`. Se inyecta externamente para asegurar que el secreto de firma de tokens sea único y no esté hardcodeado en el repositorio.

## 6. Ciclo de Vida (Automation Readiness)
La infraestructura está diseñada para ser gestionada íntegramente por un orquestador (GitHub Actions) con soporte para:
1.  **Plan:** Validación de cambios sin aplicar.
2.  **Apply:** Despliegue incremental de recursos.
3.  **Destroy:** Limpieza total del entorno para ahorro de costes.
