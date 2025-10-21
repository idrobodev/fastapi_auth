# FastAPI Authentication Backend

Backend de autenticación y gestión de usuarios construido con FastAPI para el dashboard de usuarios del sistema. Este backend proporciona servicios de login, logout, gestión de usuarios con roles y control de acceso basado en roles.

## Requisitos del Sistema

Basado en el análisis del código frontend de React, el backend debe implementar las siguientes funcionalidades:

## Lista de Tareas de Desarrollo

### Configuración del Proyecto
- [ ] Configurar estructura del proyecto FastAPI con directorios apropiados (app/, models/, routers/, utils/)
- [ ] Crear requirements.txt con dependencias necesarias (fastapi, uvicorn, sqlalchemy, python-jose, bcrypt, etc.)
- [ ] Configurar Docker para contenerización
- [ ] Agregar configuración de entorno para base de datos, JWT secret, etc.

### Base de Datos y Modelos
- [x] Configurar modelos de base de datos usando SQLAlchemy (modelo User con id, email, password_hash, role, created_at, updated_at)
- [x] Configurar conexión a base de datos SQLite y manejo de sesiones
- [x] Crear tabla de usuarios automáticamente con SQLAlchemy

### Seguridad y Autenticación
- [ ] Implementar hash de contraseñas y verificación usando bcrypt
- [ ] Configurar generación y validación de tokens JWT
- [ ] Implementar middleware de control de acceso basado en roles (ADMINISTRADOR vs CONSULTA)

### Endpoints de Autenticación
- [ ] **POST /auth/login** - Validar credenciales (JSON: `{"email": "...", "password": "..."}`) y retornar token JWT con información del usuario
- [ ] **POST /auth/logout** - Invalidar token si es necesario
- [ ] **POST /auth/reset-password** - Enviar email de reset o implementar flujo de reset de contraseña
- [ ] **PUT /auth/profile** - Actualizar perfil de usuario (requiere autenticación)
- [ ] **GET /auth/permission** - Verificar si usuario tiene rol requerido (requiere autenticación)

### Endpoints de Gestión de Usuarios
- [ ] **GET /usuarios** - Listar todos los usuarios (solo administradores)
- [ ] **POST /usuarios** - Crear nuevo usuario (solo administradores)
- [ ] **PUT /usuarios/{id}** - Actualizar usuario (solo administradores)
- [ ] **DELETE /usuarios/{id}** - Eliminar usuario (solo administradores)

### Validación y Manejo de Errores
- [ ] Agregar validación de entrada usando modelos Pydantic
- [ ] Implementar manejo de errores y códigos de estado HTTP apropiados
- [ ] Configurar middleware CORS para permitir requests del frontend React

### Utilidades y Monitoreo
- [ ] Agregar endpoint de health check (/health)
- [ ] Implementar logging apropiado
- [ ] Probar todos los endpoints con autenticación y autorización correcta

## Arquitectura

El backend está diseñado para trabajar con el frontend React existente que espera:
- API de autenticación en `http://localhost:8080/api`
- API de dashboard en `http://localhost:8000/api`

Sin embargo, este backend consolida ambas funcionalidades en un solo servicio FastAPI.

## Base de Datos

El proyecto utiliza **SQLite** como base de datos, configurada automáticamente con SQLAlchemy. El archivo de base de datos `fastapi_auth.db` se crea automáticamente en el directorio del proyecto.

### Usuarios por Defecto

Al iniciar la aplicación por primera vez, se crean automáticamente dos usuarios de prueba:

- **Administrador**: `admin@example.com` / `admin123`
- **Consulta**: `consulta@example.com` / `consulta123`

## Roles del Sistema

- **ADMINISTRADOR**: Acceso completo a gestión de usuarios y todas las funcionalidades
- **CONSULTA**: Acceso limitado, solo lectura en algunas secciones

## Tecnologías

- **FastAPI**: Framework web moderno y rápido
- **SQLAlchemy**: ORM para base de datos con SQLite
- **Pydantic**: Validación de datos
- **JWT**: Autenticación basada en tokens
- **SHA-256**: Hash de contraseñas con salt
- **Docker**: Contenerización

## Instalación y Ejecución

```bash
# Instalar dependencias
pip install -r requirements.txt

# Ejecutar con uvicorn
uvicorn main:app --reload --host 0.0.0.0 --port 8080
```

## Documentación API

La documentación automática estará disponible en `/docs` cuando el servidor esté ejecutándose.