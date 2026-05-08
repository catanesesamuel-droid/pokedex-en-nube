# PokéDex Cloud ⚡

Aplicación web PokéDex moderna y segura, diseñada para entrenadores que buscan gestionar sus colecciones en la nube. Explora datos de la PokeAPI, construye equipos competitivos y personaliza tu perfil, todo respaldado por una infraestructura robusta en Microsoft Azure.

---

## 📚 Documentación del Proyecto

Para mantener este README ligero y organizado, hemos dividido la información detallada en documentos específicos:

### 🎨 Frontend
- **[Guía Genérica](./docs/frontend_generic.md):** Funcionalidades, diseño y experiencia de usuario.
- **[Guía Técnica](./docs/frontend_technical.md):** Arquitectura SPA, integración con APIs y estrategias de despliegue.

### ⚙️ Backend
- **[Guía Genérica](./docs/backend_generic.md):** Capacidades del servidor, gestión de datos y seguridad.
- **[Guía Técnica](./docs/backend_technical.md):** Detalles de Azure Functions, esquema de Cosmos DB y referencia de la API.

---

## 📂 Estructura del Proyecto

```text
├── docs/                   # Documentación detallada (técnica y genérica)
├── backend/                # Código de las Azure Functions (Python)
│   ├── admin/              # Gestión administrativa
│   ├── auth/               # Autenticación (JWT)
│   ├── favorites/          # Gestión de favoritos
│   ├── pokemon/            # Integración con PokeAPI
│   ├── shared/             # Lógica común y DB
│   ├── team/               # Gestión de equipos
│   └── users/              # Perfil y preferencias
├── frontend/               # Interfaz de usuario (HTML/JS)
├── infra/                  # Infraestructura como Código (Terraform)
└── README.md               # Resumen del proyecto y guía rápida
```

---

## 🏗️ Arquitectura del Sistema

```
┌──────────────────────────────────────────────────────────┐
│                     Azure (rg-pokedex)                   │
│                                                          │
│  ┌─────────────┐    ┌──────────────┐    ┌─────────────┐ │
│  │  Static     │    │  Azure       │    │  CosmosDB   │ │
│  │  Website    │───▶│  Functions   │───▶│  (NoSQL)    │ │
│  │  (Storage)  │    │  Python 3.11 │    │             │ │
│  └─────────────┘    └──────────────┘    └─────────────┘ │
│                            │                            │
│                     ┌──────┴──────┐                     │
│                     │  Key Vault  │                     │
│                     │  (secretos) │                     │
│                     └─────────────┘                     │
└──────────────────────────────────────────────────────────┘
                            │
                     ┌──────▼──────┐
                     │  PokeAPI    │
                     │ (externa)   │
                     └─────────────┘
```

**Servicios Azure clave:** Azure Functions (Backend), CosmosDB (Base de datos), Storage Account (Frontend estático) y Key Vault (Seguridad).

### 🔄 Flujo de Datos
1.  **Frontend:** El usuario interactúa con la Web App.
2.  **API:** El frontend consume la API de Azure Functions enviando el token JWT.
3.  **Secretos:** Las funciones recuperan de forma segura el secreto JWT y la clave de Cosmos DB desde **Key Vault** mediante una Identidad Administrada.
4.  **Persistencia:** Los datos de usuarios, favoritos y equipos se gestionan en **Cosmos DB**.
5.  **PokeAPI:** Los datos de los Pokémon se obtienen en tiempo real desde la API externa oficial.

---

## 🚀 Despliegue Rápido (Terraform)

El proyecto utiliza **Terraform** para automatizar la creación de toda la infraestructura necesaria.

1.  **Preparar entorno:** Tener Azure CLI y Terraform instalados.
2.  **Configurar secretos:** Crear `pokedex-infra/terraform.tfvars` con tu `jwt_secret`.
3.  **Desplegar:**
    ```bash
    cd pokedex-infra
    terraform init && terraform apply
    ```
4.  **Publicar código:** Desplegar el backend con Azure Functions Core Tools y subir el `index.html` al Storage Account.

---

## 🛠️ Desarrollo Local

Si prefieres ejecutar el proyecto localmente para desarrollo:

1.  **Backend:** Instalar dependencias y arrancar con Azure Functions Core Tools.
    ```bash
    cd backend
    pip install -r requirements.txt
    func start
    ```
2.  **Frontend:** Configurar la URL de la API local y servir el archivo estático.
    ```bash
    cd frontend
    python -m http.server 5500
    ```

---

## 🔐 Seguridad

- **Cifrado:** Contraseñas hasheadas con **bcrypt**.
- **Autenticación:** Tokens **JWT** seguros con expiración controlada.
- **Protección de Secretos:** Integración nativa con **Azure Key Vault**.
- **Identidad:** Uso de **Managed Identities** para comunicación segura entre servicios sin necesidad de contraseñas en el código.

---

## 🛠️ Tecnologías Utilizadas

| Capa | Tecnologías |
|------|-----------|
| **Frontend** | HTML5, CSS3 (Vanilla), JavaScript (Vanilla) |
| **Backend** | Python 3.11, Azure Functions v2 |
| **Persistencia** | Azure CosmosDB (NoSQL) |
| **Seguridad** | JWT, Bcrypt, Azure Key Vault |
| **Infraestructura** | Terraform |

---

## 🤝 Contribución y Reportes

¿Encontraste un bug o tienes una sugerencia? ¡Siéntete libre de abrir un *issue* o enviar un *pull request*!

---
*Desarrollado con ❤️ para entrenadores Pokémon y entusiastas de la seguridad en la nube.*
