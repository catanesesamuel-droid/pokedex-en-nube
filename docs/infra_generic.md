# Arquitectura de Infraestructura (Visión General)

## Introducción
Esta documentación describe la base tecnológica del proyecto Pokedex desde una perspectiva de alto nivel. El objetivo es explicar cómo se utiliza la **Infraestructura como Código (IaC)** para crear un entorno seguro, escalable y eficiente en la nube de Microsoft Azure.

## 1. El concepto de "Nube Gestionada"
En lugar de configurar servidores manualmente, este proyecto utiliza un enfoque **Serverless (Sin Servidor)**. Esto significa que no gestionamos máquinas virtuales; Azure se encarga de la infraestructura subyacente, permitiéndonos centrar el esfuerzo en el código y la seguridad.

### Beneficios para este Proyecto:
*   **Coste Eficiente:** Al ser un proyecto universitario, el uso de planes de "Consumo" asegura que solo se paga (o se gastan créditos) cuando la aplicación se usa.
*   **Escalabilidad:** Si miles de usuarios entraran a la Pokedex a la vez, Azure ampliaría los recursos automáticamente.
*   **Repetibilidad:** Gracias a Terraform, si borramos toda la infraestructura por error, podemos recrearla exactamente igual en pocos minutos.

## 2. Los Pilares de la Aplicación

### A. La Puerta de Entrada (Frontend)
El frontend de la Pokedex (HTML, CSS y JavaScript) no necesita un servidor complejo. Se almacena en un **Azure Storage Account** configurado como sitio web estático. Es extremadamente rápido y seguro, ya que no permite la ejecución de scripts maliciosos en el lado del servidor.

### B. El Motor de Datos (Cosmos DB)
Toda la información de los usuarios y sus equipos se guarda en **Azure Cosmos DB**. Es una base de datos NoSQL que destaca por su baja latencia (rapidez) y su capacidad de organizar datos de forma flexible (documentos JSON).

### C. El Cerebro (Azure Functions)
El código Python que procesa los registros, logins y búsquedas vive en **Azure Functions**. Estas funciones se activan mediante peticiones HTTP desde el frontend y son las encargadas de comunicarse con la base de datos y el cofre de secretos.

### D. El Cofre de Seguridad (Key Vault)
**Azure Key Vault** es el componente más crítico para la seguridad. Aquí es donde guardamos:
*   La clave maestra de la base de datos.
*   El secreto para firmar los tokens de seguridad (JWT).
Ningún humano ni desarrollador debería ver estas claves en el código fuente; solo la aplicación tiene permiso para consultarlas.

## 3. Flujo de Funcionamiento
1.  El usuario abre la URL de la Pokedex (Storage Account).
2.  El navegador descarga el HTML/JS y solicita datos al backend (Azure Functions).
3.  La Azure Function se despierta, pide al Key Vault la clave secreta.
4.  Con esa clave, consulta los datos en Cosmos DB.
5.  Devuelve la respuesta al usuario de forma segura.

---
*Este documento es parte de la documentación académica para la asignatura de Seguridad en la Nube.*
