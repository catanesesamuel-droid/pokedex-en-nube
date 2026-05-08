# PokéDex Cloud - Documentación Genérica del Backend

## ☁️ Introducción
El backend de PokéDex Cloud es el motor que permite la persistencia y seguridad de la aplicación. Proporciona una API robusta y escalable que gestiona los datos de los usuarios, sus preferencias y sus colecciones de Pokémon de forma centralizada en la nube.

## 🛠️ Funcionalidades del Servidor

### 1. Seguridad y Usuarios
- **Gestión de Cuentas:** Permite el registro de nuevos entrenadores y el acceso seguro mediante credenciales.
- **Protección de Datos:** Implementa autenticación basada en tokens para asegurar que cada usuario solo acceda a su propia información.
- **Roles:** Soporte para usuarios normales y administradores.

### 2. Gestión de Datos
- **Favoritos y Equipos:** Almacena de forma persistente los pokémons que cada usuario marca como favoritos o añade a su equipo de combate.
- **Perfiles:** Guarda las preferencias de cada entrenador (como el tema de la interfaz) y sus datos de perfil.

### 3. Panel de Administración
- **Control de Usuarios:** Permite a los administradores listar todos los usuarios, bloquear cuentas sospechosas o cambiar roles de usuario.
- **Reportes:** Proporciona visibilidad sobre la actividad y el estado de la plataforma.

## 🏗️ Infraestructura y Tecnología
El backend está construido utilizando tecnologías de vanguardia en la nube para garantizar disponibilidad y rendimiento:
- **Azure Functions:** Arquitectura "Serverless" que escala automáticamente según la demanda y solo consume recursos cuando se realizan peticiones.
- **Python:** Lenguaje de programación utilizado para la lógica de los servicios.
- **Cosmos DB:** Base de datos NoSQL de alto rendimiento para el almacenamiento de documentos (usuarios, favoritos, equipos).
- **JWT (JSON Web Tokens):** Estándar de la industria para la transmisión segura de información de autenticación.

## 📡 Endpoints Principales
La API está organizada en varios módulos:
- `/auth`: Para registro, login y logout.
- `/users`: Para la gestión del perfil y preferencias.
- `/pokemon`: Proxy y búsqueda avanzada de datos.
- `/favorites`: Gestión de la lista de favoritos.
- `/team`: Configuración y edición del equipo Pokémon.
- `/mgmt`: Herramientas exclusivas para administradores.
