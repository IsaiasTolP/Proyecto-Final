# Proyecto-Final
Este repositorio corresponde al proyecto final de 2º DAW

## Requisitos del proyecto
1. Módulo APL: Auntenticación y roles
- Inicio de sesión: Los jugadores deberán iniciar sesión par acceder al juego.
- Roles:
    - Administrador: Puede gestionar cuentas y contenido de la aplicación
    - Jugador: Solo puede Jugar, acceder a perfiles y estadísticas
- Gestión de usuarios: Panel de gestión para el administrador, posiblemente el de Django por defecto.

2. Modulo EIE/FOL: Marketing y sostenibilidad
- Plan de marketing
- Plan de sostenibilidad

3. Módulo DEW: Vue.js
- Interfaz dinámica y reactiva para jugar
- Modularidad: División de la aplicación en componentes (Menús, Juego, Estadísticas, etc)
- Gestión de comunicación con Backend: Uso de Vuex o fetch/axios

4. Módulo DOR: Diseño con Bootstrap
- Uso de Bootstrap para su uso multiplataforma entre dispositivos
- Implementación de accesibilidad:
    - Soporte de navegación por teclado
    - Contrastes adecuados

5. Módulo DSW: Backend con Django
- Modelos y ORM: Define modelos para los jugadores, partidas, puntuaciones, etc.
- API REST: Creación de endpoints para registro de partidas, envio de respuestas, etc.
- Autenticación: Uso de Django Rest Framework (DRF) para manejo de sesiones seguras.
- Tareas desacopladas: Sistema de clasificaciones global calculada en segundo plano mediante Celery y Redis

## Tecnologías

Frontend: Vue.ts + Bootstrap
Backend: Django + DRF
Tareas asíncronas: Celery + Redis
Base de Datos: PostgreSQL (SQLite durante desarrollo)
Pruebas: Vite + @vue/test-utils + @testing-library/vue
Control de versiones: Git + Github
