# PokéDex Cloud - Documentación Técnica del Frontend

## 🏗️ Arquitectura
El frontend de PokéDex Cloud está diseñado como una **Single Page Application (SPA)** contenida principalmente en un único archivo `index.html`. Utiliza técnicas modernas de manipulación del DOM y gestión de estado en el lado del cliente sin depender de frameworks pesados.

### Componentes de la Arquitectura:
- **Navegación basada en DOM:** En lugar de un enrutador complejo, la aplicación alterna entre diferentes secciones (páginas) mediante la clase CSS `.active` y la función `showPage(pageId)`.
- **Gestión de Estado:** Utiliza variables globales de JavaScript para el estado actual (usuario logueado, lista de pokémons, página actual) y `LocalStorage` para la persistencia del token JWT y el tema elegido.
- **Estilos:** Implementa **Variables CSS** (Custom Properties) para soportar el cambio dinámico de temas (Dark/Light) de forma eficiente.

## 🔌 Integración con APIs

La aplicación consume datos de dos fuentes principales:
1. **PokéDex Backend (Azure Functions):** Para autenticación, gestión de favoritos, equipos, perfiles de usuario y herramientas de administración.
2. **PokeAPI (v2):** Para obtener los datos generales de los pokémons (imágenes, tipos, estadísticas) de forma directa y eficiente.

### Comunicación:
- Se utiliza la API nativa `fetch` de JavaScript para realizar peticiones HTTP.
- **Autenticación:** Todas las peticiones al backend de PokéDex incluyen el token JWT en el encabezado `Authorization: Bearer <token>`.

## 📦 Estructura de Archivos
- `index.html`: Contiene toda la estructura HTML, los estilos CSS y la lógica JavaScript (si no se ha extraído a archivos externos).
- `INTEGRATION.md`: Documento de referencia para la configuración de la URL de la API y el despliegue.

## 🚀 Despliegue y Configuración
El frontend es estático, lo que permite múltiples opciones de despliegue en Azure:
- **Azure Static Web Apps:** La opción recomendada que ofrece CI/CD nativo con GitHub.
- **Azure Blob Storage:** Alojamiento de bajo coste habilitando la función de "Sitio web estático".

### Configuración Necesaria:
En el código JavaScript, se debe configurar la variable `API_BASE` con la URL de la Function App desplegada para que el frontend pueda comunicarse con el backend.

## 🛠️ Funciones Técnicas Clave
- `doLogin() / doRegister()`: Gestionan el flujo de autenticación.
- `renderPokemonGrid()`: Renderiza dinámicamente las tarjetas de los pokémons basándose en los datos obtenidos.
- `toggleTheme()`: Alterna las variables CSS para cambiar entre modo claro y oscuro.
- `updateTeam() / updateFavorites()`: Sincronizan el estado local con la base de datos de Cosmos DB a través del backend.
