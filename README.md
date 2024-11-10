# Next-Service

**Next-Service** es una aplicación web diseñada para conectar empresas y clientes mediante servicios personalizados. La plataforma permite a los clientes reservar servicios, mientras que las empresas pueden gestionar sus reservas y notificaciones de manera eficiente.

## Tabla de Contenidos

- [Descripción](#descripción)
- [Características](#características)
- [Instalación](#instalación)
- [Uso](#uso)
- [Tecnologías Utilizadas](#tecnologías-utilizadas)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [Contribución](#contribución)
- [Licencia](#licencia)

---

## Descripción

Next-Service permite a los usuarios registrarse como empresas o clientes. Las empresas pueden crear y gestionar sus servicios, mientras que los clientes pueden reservar estos servicios y recibir notificaciones sobre el estado de sus reservas. Es una plataforma ideal para la gestión de citas y servicios personalizados.

## Características

- **Registro e Inicio de Sesión**: Autenticación para usuarios de tipo cliente y empresa.
- **Gestión de Reservas**: Permite a los clientes reservar servicios y a las empresas gestionar estas reservas (confirmación, rechazo).
- **Notificaciones**: Notificaciones para clientes y empresas sobre el estado de las reservas.
- **Perfiles de Usuario**: Personalización de perfiles tanto para clientes como para empresas.
- **Interfaz de Administración**: Panel de administración personalizado para la gestión avanzada de servicios y reservas.


## Uso

### Clientes
Los clientes pueden registrarse, iniciar sesión, navegar por los servicios, reservar citas y recibir notificaciones sobre el estado de sus reservas.

### Empresas
Las empresas pueden registrarse, crear servicios, gestionar reservas de clientes y recibir notificaciones en tiempo real.

## Tecnologías Utilizadas

- **Django**: Framework web principal.
- **Bootstrap**: Estilos y componentes para una interfaz moderna y responsiva.
- **SQLite/PostgreSQL**: Base de datos (ajustable según las necesidades de producción).
- **HTML/CSS/JavaScript**: Estructura y diseño del frontend.
- **jQuery y Flatpickr**: Mejoras de usabilidad en el frontend.
- 
## Capturas de Pantalla
![Captura de pantalla 2024-11-10 205340](https://github.com/user-attachments/assets/fcacd33e-65a3-4a94-9cf0-dcdfa6d44904)
![Captura de pantalla 2024-11-10 205331](https://github.com/user-attachments/assets/8900152d-5428-4e1e-8c0b-f54f37a7b0fb)
![Captura de pantalla 2024-11-10 205315](https://github.com/user-attachments/assets/5bca0385-0ec5-41ee-be37-28a4f74ac3e2)
![Captura de pantalla 2024-11-10 205226](https://github.com/user-attachments/assets/9f2bbd1f-966b-4c4e-8fef-6065b63bcd4d)
![Captura de pantalla 2024-11-10 205154](https://github.com/user-attachments/assets/8596da04-0a55-4364-b961-8969e82d5904)
![Captura de pantalla 2024-11-10 205147](https://github.com/user-attachments/assets/47af440e-9433-4352-be2e-1a06ac8441d5)
![Captura de pantalla 2024-11-10 205106](https://github.com/user-attachments/assets/fb6608e4-e022-467c-bb59-493868dbacc1)
![Captura de pantalla 2024-11-10 205051](https://github.com/user-attachments/assets/77a15364-c10e-4491-8eae-dcf877679b2e)
![Captura de pantalla 2024-11-10 205004](https://github.com/user-attachments/assets/4996cc58-cef2-47bc-9161-2a07876cc3b4)

## Estructura del Proyecto

```bash
next-service/
├── bookings/         # Aplicación para gestionar reservas
├── core/             # Configuración central de la aplicación
├── notifications/    # Aplicación para gestionar notificaciones
├── services/         # Aplicación para gestión de servicios
├── users/            # Aplicación para gestionar perfiles de usuario
└── README.md         # Descripción del proyecto
