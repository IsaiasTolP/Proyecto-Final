# Backend API en Django

## Especificaciones técnicas
- **Versión de Python**: 3.13.1
- **Framework principal**: Django + Django REST Framework
- **Sistema de autenticación**: Bearer Token con SimpleJWT
- **Tareas en segundo plano**: Django-rq con Redis (en contenedor Docker)

## Librerías utilizadas
- **Autenticación**: SimpleJWT
- **Procesamiento en background**: Django-rq
- **Seguridad**: cryptography (encriptación de datos)
- **Imágenes**: django-imagekit + Pillow
- **PDF**: WeasyPrint
- **Colores**: django-colorfield

---

## Estructura de Aplicaciones

### `main`
Aplicación principal que contiene:
- Configuración base del proyecto
- Rutas principales

### `accounts`
Gestión de perfiles de usuario:
- Modelos: `Profile`, `FounderProfile`
- Serializadores
- Vistas
- Endpoints

### `contributions`
Gestión de contribuciones:
- Modelo: `Contribution`
- Serializadores
- Vistas
- Endpoints

### `PaymentMethod`
Gestión de métodos de pago:
- Modelo: `PaymentMethod`
- Serializadores
- Vistas
- Endpoints

### `projects`
Gestión de proyectos:
- Modelos: `Project`, `ProjectCategory`, `ProjectImage`
- Serializadores
- Vistas
- Endpoints

### `shared`
Recursos compartidos entre aplicaciones

### `users`
Gestión de usuarios:
- Autenticación (login, registro)
- Serializadores
- Vistas
- Endpoints

---

## Modelos de Base de Datos

### Aplicación `accounts`

#### `Profile`
Extensión del modelo User de Django con información adicional.

**Campos**:
1. `id` - Identificador único
2. `user` - Relación 1-1 con User
3. `bio` - Biografía del usuario
4. `pfp` - Imagen de perfil
5. `location` - Ubicación del usuario
6. `is_founder` - Indica si puede crear proyectos

#### `FounderProfile`
Extiende `Profile` con información para fundadores.

**Campos adicionales**:
1. `website` - Sitio web personal
2. `social_media` - Redes sociales (JSON)
3. `contact_email` - Email de contacto

---

### Aplicación `contributions`

#### `Contribution`
Representa una contribución a un proyecto.

**Campos**:
1. `id` - Identificador único
2. `amount` - Cantidad donada
3. `date` - Fecha/hora de la contribución
4. `message` - Mensaje opcional
5. `project` - Proyecto beneficiario
6. `contributor` - Usuario que contribuye
7. `payment_method` - Método de pago usado

---

### Aplicación `PaymentMethod`

#### `PaymentMethod`
Métodos de pago de usuarios.

**Campos**:
1. `id` - Identificador único
2. `user` - Usuario propietario
3. `holder_name` - Nombre del titular
4. `card_number` - Número cifrado
5. `cvv` - Código cifrado
6. `expiration_date` - Fecha de expiración

**Métodos**:
- `save_card()` - Cifra y almacena datos
- `delete()` - Eliminación segura
- `get_card_number()` - Descifra número
- `get_cvv()` - Descifra CVV
- `is_expired()` - Verifica expiración

---

### Aplicación `projects`

#### `ProjectCategory`
Categorías de proyectos.

**Campos**:
1. `id` - Identificador único
2. `category` - Nombre (único)
3. `icon` - Ícono representativo
4. `color` - Color asociado

**Métodos**:
- `__str__()` - Devuelve el nombre

#### `Project`
Proyectos de crowdfunding.

**Campos**:
1. `id` - Identificador único
2. `name` - Nombre del proyecto
3. `description` - Descripción detallada
4. `goal` - Meta de financiación
5. `start_date` - Fecha de inicio
6. `is_active` - Estado activo/inactivo
7. `category` - Categoría asociada
8. `owner` - Usuario propietario
9. `featured` - Proyecto destacado

**Propiedades**:
- `total_donated` - Suma de donaciones
- `percent_completed` - % de financiación
- `is_completed` - 100% completado

#### `ProjectImage`
Imágenes asociadas a proyectos.

**Campos**:
1. `id` - Identificador único
2. `project` - Proyecto asociado
3. `image` - Archivo de imagen

---

## Serializadores

### Aplicación `accounts`

#### `ProfileSerializer`
Serializa el modelo `Profile` incluyendo todos los campos y el usuario completo.

#### `FounderProfileSerializer`
Serializa `FounderProfile` incluyendo campos de `Profile` y usuario completo.

---

### Aplicación `contributions`

#### `ContributionSerializer`
Serializa el modelo `Contribution` con todos los campos.

**Métodos**:
- `validate_payment_method()` - Valida método de pago
- `validate_project()` - Valida proyecto

#### `SimpleContributionSerializer`
Versión simplificada con campos de solo lectura.

---

### Aplicación `PaymentMethod`

#### `PaymentMethodSerializer`
**Campos**:
- `id`, `holder_name`, `expiration_date`
- `card_number` (solo escritura)
- `cvv` (solo escritura)
- `card_last4` (solo lectura)

**Métodos**:
- `get_card_last4()` - Obtiene últimos 4 dígitos
- `create()` - Cifra y almacena datos
- `update()` - Actualiza datos cifrados

---

### Aplicación `projects`

#### `ProjectCategorySerializer`
**Campos**:
- `id`, `category`, `icon`, `color`
- `num_projects` - Total de proyectos

#### `ProjectImageSerializer`
Todos los campos del modelo.

#### `ProjectSerializer`
**Campos**:
- `id`, `name`, `description`, `goal`
- `start_date`, `is_active`, `category`
- `owner`, `project_images`
- `total_donated`, `percent_completed`, `featured`

**Campos de solo lectura**:
- `start_date`
- `total_donated`
- `percent_completed`

---

### Aplicación `users`

#### `UserSerializer`
**Campos**:
- `id`, `username`, `email`, `is_founder`
- `password` (solo escritura)

**Métodos**:
- `create()` - Crea usuario con perfil
- `update()` - Actualiza datos
- `to_representation()` - Formatea salida

#### `SimpleUserSerializer`
Versión simplificada:
- `id`, `username`, `is_founder`

#### `CustomTokenObtainPairSerializer`
Extiende SimpleJWT para autenticación personalizada.

---

## Vistas

### Aplicación `accounts`

#### `ProfileViewSet`
**Acciones**:
1. Búsqueda por ID de usuario
2. Obtener perfil del solicitante

#### `FounderProfileViewSet`
**Acciones**:
1. Búsqueda por ID de usuario
2. Obtener perfil del solicitante

---

### Aplicación `contributions`

#### `ContributionViewSet`
- Solo accesible por el dueño
- Incluye tareas de email con facturas

#### `SimpleContributionViewSet`
- Accesible por todos los autenticados
- Solo consulta (no modificación)

---

### Aplicación `PaymentMethod`

#### `PaymentMethodViewSet`
**Características**:
- Autenticación requerida
- Permisos personalizados (solo dueño)
- Filtrado por usuario
- Auto-asociación al crear

---

### Aplicación `projects`

#### `ProjectViewSet`
**Filtros**:
- Por categoría, estado, dueño
- Ordenación por fecha/meta
- Búsqueda por nombre

**Acciones**:
- `latest()` - 3 proyectos recientes
- `featured()` - Proyectos destacados

#### `ProjectCategoryViewSet`
- Incluye conteo de proyectos

#### `ProjectImageViewSet`
- Filtrado por proyecto

#### `ProjectStatsView`
Devuelve estadísticas globales:
- Total donaciones
- Número de proyectos
- Proyectos activos/completados
- Número de usuarios

---

### Aplicación `users`

#### `RegisterUserAPIView`
- Crea usuario
- Envía email de bienvenida

#### `CustomLoginView` / `LoginAPIView`
- Autenticación JWT
- Genera tokens refresh/access

#### `UserDetailView`
- Obtiene/actualiza usuario
- Permisos: solo propio usuario

# Importante para Windows: Es necesario tener unos contenedores de Docker con Django, Redis, Base de datos PostgreSQL, para funcionar en desarrollo.

## Comando para borrado de tareas encoladas en el worker (Se puede usar en el contenedor de desarrollo para impedir que se vayan acumulando tareas que no vamos a necesitar) --> rq empty default --url redis://redis:6379/0
