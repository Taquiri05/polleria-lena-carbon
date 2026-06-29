# architecture.md
# Sistema Integral de Gestión para Pollería Leña y Carbón
**Especificación de Arquitectura — Spec Driven Development (SDD)**
**Curso:** IS-489 Pruebas y Aseguramiento de Calidad — UNSCH 2026
**Versión:** 1.0.0 | **Fecha:** Junio 2026

---

## 1. VISIÓN GENERAL DE LA ARQUITECTURA

### 1.1. Patrón Arquitectónico
El sistema adopta una **arquitectura desacoplada de dos capas independientes** (Decoupled Architecture):

- **Capa Cliente (Frontend):** Single Page Application (SPA) construida con React + Vite. Se comunica con el backend exclusivamente mediante peticiones HTTP a la API REST.
- **Capa Servidor (Backend):** API REST stateless construida con Python + Flask. Expone endpoints JSON consumidos por el frontend y cualquier cliente HTTP.

La comunicación entre ambas capas se realiza mediante el protocolo **HTTP/HTTPS**, con autenticación basada en **tokens JWT** transmitidos en el header `Authorization: Bearer <token>`.

```
┌─────────────────────────────────────────────────────────────────────┐
│                        CLIENTE / BROWSER                            │
│                                                                     │
│   ┌─────────────────────────────────────────────────────────────┐   │
│   │           FRONTEND — React SPA (Vercel / Render)           │   │
│   │   React 18 · Vite · Tailwind CSS · shadcn/ui · Zustand     │   │
│   │   React Hook Form · Zod · Axios · React Router v6          │   │
│   └─────────────────────┬───────────────────────────────────────┘   │
└─────────────────────────┼───────────────────────────────────────────┘
                          │  HTTP/HTTPS — JSON — JWT
                          ▼
┌─────────────────────────────────────────────────────────────────────┐
│                  BACKEND — Flask API REST (Render / Railway)        │
│                                                                     │
│   ┌──────────────┐   ┌──────────────┐   ┌──────────────────────┐   │
│   │   ROUTES     │──▶│   SERVICES   │──▶│      MODELS          │   │
│   │ (Capa 1)     │   │ (Capa 2)     │   │   (Capa 3)           │   │
│   │ Flask        │   │ Lógica de    │   │ Flask-SQLAlchemy      │   │
│   │ Blueprints   │   │ negocio      │   │ + Marshmallow         │   │
│   └──────────────┘   └──────────────┘   └──────────┬───────────┘   │
│                                                     │               │
└─────────────────────────────────────────────────────┼───────────────┘
                                                      │  SQLAlchemy ORM
                                                      ▼
                                        ┌─────────────────────────┐
                                        │   BASE DE DATOS         │
                                        │   MySQL 8.x (InnoDB)    │
                                        │   Railway / PlanetScale │
                                        └─────────────────────────┘
```

### 1.2. Principios de Diseño
| Principio | Aplicación en el proyecto |
|-----------|--------------------------|
| **Separación de responsabilidades** | Routes solo enruta, Services contiene la lógica de negocio, Models define la estructura de datos. |
| **Testabilidad como diseño** | La capa Services es independiente de Flask y se puede probar con pytest sin levantar el servidor. |
| **Stateless API** | El servidor no mantiene sesión; cada petición lleva el JWT con la identidad del usuario. |
| **Diseño simple (SDD)** | Cada módulo contiene solo lo necesario para cumplir los requerimientos especificados en `requirements.md`. |
| **Fail-fast con respuestas estándar** | Todos los errores retornan JSON con `{"error": "mensaje"}` y el código HTTP correspondiente. |

---

## 2. ARQUITECTURA DEL BACKEND

### 2.1. Estructura de Carpetas

```
backend/
├── app/
│   ├── __init__.py                  ← Application Factory (create_app)
│   ├── extensions.py                ← Instancias de db, jwt, ma
│   ├── routes/                      ← Capa 1: Blueprints Flask
│   │   ├── __init__.py
│   │   ├── auth_routes.py           ← /api/auth
│   │   ├── reservas_routes.py       ← /api/reservas
│   │   ├── mesas_routes.py          ← /api/mesas
│   │   ├── carta_routes.py          ← /api/categorias, /api/platillos
│   │   ├── takeaway_routes.py       ← /api/takeaway
│   │   └── admin_routes.py          ← /api/admin
│   ├── services/                    ← Capa 2: Lógica de negocio (COBERTURA ≥90%)
│   │   ├── __init__.py
│   │   ├── auth_service.py
│   │   ├── reserva_service.py
│   │   ├── mesa_service.py
│   │   ├── carta_service.py
│   │   └── takeaway_service.py
│   ├── models/                      ← Capa 3: Modelos SQLAlchemy
│   │   ├── __init__.py
│   │   ├── usuario.py
│   │   ├── mesa.py
│   │   ├── reserva.py
│   │   ├── categoria.py
│   │   ├── platillo.py
│   │   ├── pedido_takeaway.py
│   │   ├── detalle_pedido.py
│   │   └── configuracion.py
│   └── schemas/                     ← Marshmallow: serialización y validación
│       ├── __init__.py
│       ├── usuario_schema.py
│       ├── reserva_schema.py
│       ├── mesa_schema.py
│       ├── carta_schema.py
│       └── takeaway_schema.py
├── tests/
│   ├── conftest.py                  ← Fixtures globales pytest (app, db, client)
│   ├── unit/
│   │   ├── test_auth_service.py
│   │   ├── test_reserva_service.py
│   │   ├── test_mesa_service.py
│   │   ├── test_carta_service.py
│   │   └── test_takeaway_service.py
│   └── integration/
│       ├── test_auth_routes.py
│       ├── test_reservas_routes.py
│       ├── test_takeaway_routes.py
│       └── test_carta_routes.py
├── config.py                        ← Configuraciones por entorno
├── requirements.txt
├── .env.example
├── run.py                           ← Punto de entrada
└── Procfile                         ← Para Render/Railway
```

### 2.2. Flujo de una Petición HTTP

```
Petición HTTP entrante
        │
        ▼
┌───────────────────┐
│   MIDDLEWARE JWT  │  ← @jwt_required() valida el token
│   (decorador)     │    Retorna 401 si token inválido/expirado
└────────┬──────────┘    Retorna 403 si rol insuficiente
         │
         ▼
┌───────────────────┐
│     ROUTE         │  ← Blueprint Flask
│  (routes/*.py)    │    Recibe request, valida schema con Marshmallow
│                   │    Llama al servicio correspondiente
└────────┬──────────┘
         │
         ▼
┌───────────────────┐
│     SERVICE       │  ← Lógica de negocio pura
│  (services/*.py)  │    Aplica reglas de negocio (RN-01..RN-10)
│                   │    Interactúa con modelos SQLAlchemy
│                   │    ← OBJETIVO COBERTURA pytest ≥ 90%
└────────┬──────────┘
         │
         ▼
┌───────────────────┐
│     MODEL         │  ← SQLAlchemy ORM
│  (models/*.py)    │    Consultas y transacciones MySQL
└────────┬──────────┘
         │
         ▼
┌───────────────────┐
│   MySQL 8.x       │
└───────────────────┘
         │
         ▼ (respuesta sube por la misma pila)
JSON Response + HTTP Status Code
```

### 2.3. Application Factory

```python
# app/__init__.py — patrón Application Factory
def create_app(config_name="development"):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    # Inicializar extensiones
    db.init_app(app)
    jwt.init_app(app)
    ma.init_app(app)
    CORS(app)

    # Registrar blueprints
    from .routes import auth_routes, reservas_routes, mesas_routes
    from .routes import carta_routes, takeaway_routes, admin_routes
    app.register_blueprint(auth_routes.bp)
    app.register_blueprint(reservas_routes.bp)
    app.register_blueprint(mesas_routes.bp)
    app.register_blueprint(carta_routes.bp)
    app.register_blueprint(takeaway_routes.bp)
    app.register_blueprint(admin_routes.bp)

    return app
```

### 2.4. Configuración por Entornos

```python
# config.py
class Config:
    SECRET_KEY = os.getenv("SECRET_KEY")
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=8)
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL_DEV")

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"  # BD en memoria para pytest
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=5)

class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")

config = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
}
```

> **Decisión de diseño:** En los tests unitarios se usa SQLite en memoria para aislar las pruebas de la base de datos de producción y garantizar velocidad de ejecución. Los tests de integración usan una base MySQL de prueba separada.

---

## 3. REFERENCIA COMPLETA DE ENDPOINTS REST API

**URL Base:** `https://api.polleria-lenacarbon.onrender.com/api`
**Formato:** JSON en todas las peticiones y respuestas.
**Autenticación:** `Authorization: Bearer <JWT_TOKEN>` en headers para rutas protegidas.

**Leyenda de roles:**
- 🔓 Público — sin autenticación
- 🔐 Autenticado — cualquier rol con JWT válido
- 👷 Recepcionista — rol RECEPCIONISTA o ADMIN
- 👑 Admin — solo rol ADMIN

---

### 3.1. Módulo AUTH — `/api/auth`

| # | Método | Ruta | Descripción | Acceso | Body requerido | Respuesta exitosa |
|---|--------|------|-------------|--------|----------------|-------------------|
| 1 | `POST` | `/api/auth/login` | Autenticación de usuario con credenciales | 🔓 | `{email, password}` | `200` `{access_token, usuario:{id,nombre,email,rol}}` |
| 2 | `POST` | `/api/auth/logout` | Invalidación del token activo | 🔐 | — | `200` `{message: "Sesión cerrada correctamente"}` |
| 3 | `PUT` | `/api/auth/cambiar-password` | Cambio de contraseña del usuario autenticado | 🔐 | `{password_actual, password_nueva}` | `200` `{message: "Contraseña actualizada"}` |
| 4 | `GET` | `/api/auth/perfil` | Obtener datos del usuario autenticado | 🔐 | — | `200` `{id, nombre, email, rol}` |

**Errores comunes del módulo AUTH:**
- `401` → Credenciales inválidas / token expirado
- `403` → Cuenta desactivada / rol insuficiente
- `400` → Campos faltantes o contraseña actual incorrecta

---

### 3.2. Módulo USUARIOS — `/api/usuarios`

| # | Método | Ruta | Descripción | Acceso | Body requerido | Respuesta exitosa |
|---|--------|------|-------------|--------|----------------|-------------------|
| 5 | `GET` | `/api/usuarios` | Listar todos los usuarios del sistema | 👑 | — | `200` `[{id, nombre, email, rol, activo}]` |
| 6 | `POST` | `/api/usuarios` | Crear nuevo usuario (Recepcionista o Admin) | 👑 | `{nombre, email, password, rol}` | `201` `{id, nombre, email, rol, activo}` |
| 7 | `GET` | `/api/usuarios/:id` | Obtener detalle de un usuario | 👑 | — | `200` `{id, nombre, email, rol, activo, created_at}` |
| 8 | `PUT` | `/api/usuarios/:id` | Editar datos de un usuario | 👑 | `{nombre?, email?, rol?}` | `200` `{id, nombre, email, rol}` |
| 9 | `PATCH` | `/api/usuarios/:id/estado` | Activar o desactivar un usuario | 👑 | `{activo: bool}` | `200` `{message: "Estado actualizado"}` |

**Errores comunes del módulo USUARIOS:**
- `409` → Email ya registrado
- `404` → Usuario no encontrado
- `400` → Datos inválidos o rol no permitido

---

### 3.3. Módulo MESAS — `/api/mesas`

| # | Método | Ruta | Descripción | Acceso | Body requerido | Respuesta exitosa |
|---|--------|------|-------------|--------|----------------|-------------------|
| 10 | `GET` | `/api/mesas` | Listar todas las mesas activas | 👷 | — | `200` `[{id, numero, capacidad, tipo_ocasion, activo}]` |
| 11 | `POST` | `/api/mesas` | Registrar nueva mesa | 👑 | `{numero, capacidad, tipo_ocasion}` | `201` `{id, numero, capacidad, tipo_ocasion}` |
| 12 | `PUT` | `/api/mesas/:id` | Editar datos de una mesa | 👑 | `{numero?, capacidad?, tipo_ocasion?}` | `200` `{id, numero, capacidad, tipo_ocasion}` |
| 13 | `PATCH` | `/api/mesas/:id/estado` | Activar o desactivar una mesa | 👑 | `{activo: bool}` | `200` `{message: "Estado actualizado"}` |

**Errores comunes del módulo MESAS:**
- `409` → Número de mesa duplicado
- `404` → Mesa no encontrada
- `400` → `tipo_ocasion` no válido (debe ser: familiar, romantica, reunion)

---

### 3.4. Módulo RESERVAS — `/api/reservas`

| # | Método | Ruta | Descripción | Acceso | Body requerido | Respuesta exitosa |
|---|--------|------|-------------|--------|----------------|-------------------|
| 14 | `POST` | `/api/reservas` | Crear reserva con asignación automática de mesa | 🔓 | `{cliente_nombre, cliente_contacto, fecha, hora, num_personas, tipo_ocasion}` | `201` `{id, codigo_confirmacion, mesa:{numero}, fecha, hora, estado}` |
| 15 | `GET` | `/api/reservas/disponibilidad` | Consultar disponibilidad por fecha y tipo | 🔓 | Query: `?fecha=&hora=&tipo_ocasion=&num_personas=` | `200` `{disponible: bool, horarios_sugeridos?: []}` |
| 16 | `GET` | `/api/reservas` | Listar reservas (con filtros) | 👷 | Query: `?fecha=&estado=` | `200` `[{id, cliente_nombre, fecha, hora, mesa, estado, codigo_confirmacion}]` |
| 17 | `GET` | `/api/reservas/:id` | Obtener detalle de una reserva | 👷 | — | `200` `{id, cliente_nombre, cliente_contacto, fecha, hora, num_personas, tipo_ocasion, estado, mesa, created_at}` |
| 18 | `PATCH` | `/api/reservas/:id/estado` | Actualizar estado de reserva | 👷 | `{estado}` (confirmada/completada/cancelada) | `200` `{id, estado}` |
| 19 | `POST` | `/api/reservas/cancelar` | Cliente cancela su reserva con código | 🔓 | `{codigo_confirmacion}` | `200` `{message: "Reserva cancelada correctamente"}` |

**Errores comunes del módulo RESERVAS:**
- `409` → No hay mesa disponible para el horario y tipo solicitado
- `400` → Fecha pasada / hora inválida / campos faltantes
- `404` → Código de confirmación no encontrado
- `422` → Cancelación fuera de plazo (menos de 1 hora de anticipación)
- `422` → Transición de estado inválida

---

### 3.5. Módulo CARTA DIGITAL — `/api/categorias` y `/api/platillos`

| # | Método | Ruta | Descripción | Acceso | Body requerido | Respuesta exitosa |
|---|--------|------|-------------|--------|----------------|-------------------|
| 20 | `GET` | `/api/categorias` | Listar categorías activas con sus platillos | 🔓 | — | `200` `[{id, nombre, platillos:[{id,nombre,precio,imagen_url}]}]` |
| 21 | `POST` | `/api/categorias` | Crear nueva categoría | 👑 | `{nombre, descripcion}` | `201` `{id, nombre, descripcion}` |
| 22 | `PUT` | `/api/categorias/:id` | Editar categoría | 👑 | `{nombre?, descripcion?}` | `200` `{id, nombre, descripcion}` |
| 23 | `DELETE` | `/api/categorias/:id` | Eliminar categoría (sin platillos activos) | 👑 | — | `200` `{message: "Categoría eliminada"}` |
| 24 | `GET` | `/api/platillos` | Listar todos los platillos (con filtro por categoría) | 🔓 | Query: `?categoria_id=&activo=` | `200` `[{id, nombre, descripcion, precio, imagen_url, activo, categoria}]` |
| 25 | `POST` | `/api/platillos` | Crear nuevo platillo | 👑 | `{nombre, descripcion, precio, imagen_url, categoria_id}` | `201` `{id, nombre, precio, categoria}` |
| 26 | `PUT` | `/api/platillos/:id` | Editar datos de un platillo | 👑 | `{nombre?, descripcion?, precio?, imagen_url?, categoria_id?}` | `200` `{id, nombre, precio, categoria}` |
| 27 | `PATCH` | `/api/platillos/:id/estado` | Activar o desactivar platillo de la carta | 👑 | `{activo: bool}` | `200` `{message: "Visibilidad actualizada"}` |

**Errores comunes del módulo CARTA:**
- `409` → No se puede eliminar categoría con platillos activos (RN-09)
- `404` → Categoría o platillo no encontrado
- `400` → Precio negativo / campos obligatorios faltantes

---

### 3.6. Módulo TAKEAWAY — `/api/takeaway`

| # | Método | Ruta | Descripción | Acceso | Body requerido | Respuesta exitosa |
|---|--------|------|-------------|--------|----------------|-------------------|
| 28 | `POST` | `/api/takeaway` | Crear pedido takeaway con ítems | 🔓 | `{cliente_nombre, cliente_contacto, items:[{platillo_id, cantidad}]}` | `201` `{id, codigo_seguimiento, total, estado, items}` |
| 29 | `GET` | `/api/takeaway/estado/:codigo` | Consultar estado del pedido por código | 🔓 | — | `200` `{codigo_seguimiento, estado, total, items, created_at}` |
| 30 | `GET` | `/api/takeaway` | Listar pedidos takeaway (con filtros) | 👷 | Query: `?fecha=&estado=` | `200` `[{id, cliente_nombre, total, estado, codigo_seguimiento, created_at}]` |
| 31 | `GET` | `/api/takeaway/:id` | Obtener detalle completo de un pedido | 👷 | — | `200` `{id, cliente_nombre, cliente_contacto, total, estado, codigo_seguimiento, items:[{platillo, cantidad, precio_unitario}]}` |
| 32 | `PATCH` | `/api/takeaway/:id/estado` | Actualizar estado del pedido | 👷 | `{estado}` (en_preparacion/listo/entregado/cancelado) | `200` `{id, estado}` |

**Errores comunes del módulo TAKEAWAY:**
- `400` → Items vacíos / platillo_id inválido / cantidad ≤ 0
- `422` → Platillo desactivado incluido en el pedido
- `422` → Cancelación de pedido no en estado "recibido" (RN-05)
- `404` → Código de seguimiento no encontrado

---

### 3.7. Módulo ADMINISTRACIÓN — `/api/admin`

| # | Método | Ruta | Descripción | Acceso | Body requerido | Respuesta exitosa |
|---|--------|------|-------------|--------|----------------|-------------------|
| 33 | `GET` | `/api/admin/dashboard` | Métricas del día (reservas, pedidos, ingresos) | 👑 | — | `200` `{reservas_hoy, pedidos_hoy, ingresos_estimados, platillos_top:[]}` |
| 34 | `GET` | `/api/admin/configuracion` | Obtener configuración general del sistema | 👑 | — | `200` `{nombre_negocio, horario_apertura, horario_cierre, contacto, ...}` |
| 35 | `PUT` | `/api/admin/configuracion` | Actualizar parámetros de configuración | 👑 | `{clave, valor}` o `[{clave, valor}]` | `200` `{message: "Configuración actualizada"}` |

**Errores comunes del módulo ADMIN:**
- `400` → Clave de configuración no reconocida
- `403` → Acceso denegado (rol insuficiente)

---

### 3.8. Resumen de Endpoints

| Total endpoints | Públicos 🔓 | Autenticados 🔐 | Recepcionista 👷 | Admin 👑 |
|-----------------|------------|-----------------|-----------------|---------|
| **35** | 9 | 2 | 7 | 17 |

---

## 4. ARQUITECTURA DEL FRONTEND

### 4.1. Estructura de Carpetas

```
frontend/
├── public/
│   └── favicon.ico
├── src/
│   ├── main.jsx                     ← Punto de entrada React
│   ├── App.jsx                      ← Router principal (React Router v6)
│   ├── components/                  ← Componentes reutilizables
│   │   ├── ui/                      ← shadcn/ui (Button, Card, Input, etc.)
│   │   ├── layout/
│   │   │   ├── Navbar.jsx
│   │   │   ├── Sidebar.jsx          ← Panel admin
│   │   │   └── Footer.jsx
│   │   ├── reservas/
│   │   │   ├── FormularioReserva.jsx
│   │   │   └── TarjetaReserva.jsx
│   │   ├── carta/
│   │   │   ├── TarjetaPlatillo.jsx
│   │   │   └── FiltroCategorias.jsx
│   │   └── takeaway/
│   │       ├── CarritoTakeaway.jsx
│   │       └── TarjetaPedido.jsx
│   ├── pages/                       ← Vistas principales
│   │   ├── public/
│   │   │   ├── HomePage.jsx         ← Carta digital pública
│   │   │   ├── ReservaPage.jsx      ← Formulario de reserva
│   │   │   ├── TakeawayPage.jsx     ← Pedido para llevar
│   │   │   └── SeguimientoPage.jsx  ← Consulta estado pedido
│   │   ├── auth/
│   │   │   └── LoginPage.jsx
│   │   ├── recepcionista/
│   │   │   ├── ReservasDiaPage.jsx
│   │   │   └── PedidosDiaPage.jsx
│   │   └── admin/
│   │       ├── DashboardPage.jsx
│   │       ├── CartaPage.jsx
│   │       ├── UsuariosPage.jsx
│   │       ├── MesasPage.jsx
│   │       └── ConfiguracionPage.jsx
│   ├── services/                    ← Llamadas Axios a la API
│   │   ├── api.js                   ← Instancia Axios con interceptors JWT
│   │   ├── authService.js
│   │   ├── reservaService.js
│   │   ├── cartaService.js
│   │   └── takeawayService.js
│   ├── store/                       ← Zustand stores
│   │   ├── authStore.js             ← Estado de autenticación + token
│   │   ├── cartaStore.js            ← Estado de la carta y carrito
│   │   └── reservaStore.js
│   ├── schemas/                     ← Zod schemas para validación
│   │   ├── reservaSchema.js
│   │   ├── takeawaySchema.js
│   │   └── authSchema.js
│   └── utils/
│       ├── formatters.js            ← Formateo de fechas y precios (PEN)
│       └── constants.js             ← TIPOS_OCASION, ESTADOS_PEDIDO, etc.
├── .env.example
├── index.html
├── package.json
├── tailwind.config.js
└── vite.config.js
```

### 4.2. Rutas del Frontend (React Router v6)

| Ruta | Componente | Acceso | Descripción |
|------|------------|--------|-------------|
| `/` | `HomePage` | Público | Carta digital y accesos principales |
| `/reservas` | `ReservaPage` | Público | Formulario para crear reserva |
| `/takeaway` | `TakeawayPage` | Público | Pedido para llevar |
| `/seguimiento/:codigo` | `SeguimientoPage` | Público | Estado del pedido takeaway |
| `/login` | `LoginPage` | Público | Inicio de sesión staff |
| `/recepcion/reservas` | `ReservasDiaPage` | 👷 Recepcionista | Reservas del día |
| `/recepcion/pedidos` | `PedidosDiaPage` | 👷 Recepcionista | Pedidos takeaway activos |
| `/admin` | `DashboardPage` | 👑 Admin | Panel principal con métricas |
| `/admin/carta` | `CartaPage` | 👑 Admin | Gestión de categorías y platillos |
| `/admin/usuarios` | `UsuariosPage` | 👑 Admin | Gestión de cuentas de usuario |
| `/admin/mesas` | `MesasPage` | 👑 Admin | Gestión de mesas |
| `/admin/configuracion` | `ConfiguracionPage` | 👑 Admin | Parámetros del sistema |

### 4.3. Gestión del Estado con Zustand

```javascript
// store/authStore.js — patrón de store de autenticación
const useAuthStore = create((set) => ({
  usuario: null,
  token: null,
  isAuthenticated: false,

  login: (usuario, token) => {
    localStorage.setItem("token", token);
    set({ usuario, token, isAuthenticated: true });
  },

  logout: () => {
    localStorage.removeItem("token");
    set({ usuario: null, token: null, isAuthenticated: false });
  },
}));
```

### 4.4. Interceptor Axios con JWT

```javascript
// services/api.js
const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL,
  headers: { "Content-Type": "application/json" },
});

// Adjuntar token automáticamente
api.interceptors.request.use((config) => {
  const token = localStorage.getItem("token");
  if (token) config.headers.Authorization = `Bearer ${token}`;
  return config;
});

// Manejar token expirado globalmente
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      useAuthStore.getState().logout();
      window.location.href = "/login";
    }
    return Promise.reject(error);
  }
);
```

---

## 5. ARQUITECTURA DE BASE DE DATOS

### 5.1. Diagrama Entidad-Relación (textual)

```
USUARIO                    MESA
──────────────────         ──────────────────────
PK  id INT                 PK  id INT
    nombre VARCHAR(100)         numero INT UNIQUE
    email VARCHAR(150) UQ       capacidad TINYINT
    password_hash VARCHAR(255)  tipo_ocasion ENUM
    rol ENUM                    activo BOOLEAN
    activo BOOLEAN              (familiar/romantica/reunion)
    created_at DATETIME

        │ FK mesa_id
        ▼
RESERVA
────────────────────────────────
PK  id INT
    cliente_nombre VARCHAR(100)
    cliente_contacto VARCHAR(20)
    fecha DATE
    hora TIME
    num_personas TINYINT
    tipo_ocasion ENUM
    estado ENUM (pendiente/confirmada/completada/cancelada)
    codigo_confirmacion VARCHAR(20) UQ
FK  mesa_id INT → MESA(id)
    created_at DATETIME


CATEGORIA                  PLATILLO
──────────────────         ──────────────────────────
PK  id INT                 PK  id INT
    nombre VARCHAR(100)         nombre VARCHAR(150)
    descripcion TEXT            descripcion TEXT
    activo BOOLEAN              precio DECIMAL(8,2)
                                imagen_url VARCHAR(255)
        │ FK categoria_id        activo BOOLEAN
        ▼               FK  categoria_id INT → CATEGORIA(id)


PEDIDO_TAKEAWAY            DETALLE_PEDIDO
──────────────────────     ────────────────────────────
PK  id INT                 PK  id INT
    cliente_nombre          FK  pedido_id → PEDIDO_TAKEAWAY(id)
    cliente_contacto        FK  platillo_id → PLATILLO(id)
    total DECIMAL(10,2)         cantidad TINYINT
    estado ENUM                 precio_unitario DECIMAL(8,2)
    codigo_seguimiento UQ
    created_at DATETIME

CONFIGURACION
────────────────────────────
PK  id INT
    clave VARCHAR(100) UQ
    valor VARCHAR(255)
    (Seed: nombre_negocio, horario_apertura, horario_cierre,
           contacto, jwt_expiration_hours)
```

### 5.2. Estados y Transiciones Válidas

**Reserva:**
```
pendiente ──▶ confirmada ──▶ completada
    │               │
    └──▶ cancelada ◀┘
```

**Pedido Takeaway:**
```
recibido ──▶ en_preparacion ──▶ listo ──▶ entregado
    │
    └──▶ cancelado   (solo desde "recibido" — RN-05)
```

---

## 6. SEGURIDAD

### 6.1. Autenticación JWT

```
POST /api/auth/login
│
├── Validar email + password con bcrypt.checkpw()
├── Verificar cuenta activa
├── Generar JWT con payload:
│     { user_id, email, rol, exp: now + 8h }
└── Retornar access_token
```

- Los tokens JWT son firmados con `HS256` usando la `SECRET_KEY` del servidor.
- La clave secreta se carga exclusivamente desde variables de entorno (`.env`), nunca del código fuente.
- El tiempo de expiración es configurable desde la tabla `Configuracion` (clave: `jwt_expiration_hours`).

### 6.2. Control de Acceso por Rol

```python
# Decorador de autorización por rol
def rol_requerido(*roles):
    def decorator(fn):
        @wraps(fn)
        @jwt_required()
        def wrapper(*args, **kwargs):
            claims = get_jwt()
            if claims.get("rol") not in roles:
                return {"error": "Acceso denegado"}, 403
            return fn(*args, **kwargs)
        return wrapper
    return decorator

# Uso en rutas
@bp.route("/usuarios", methods=["POST"])
@rol_requerido("ADMIN")
def crear_usuario():
    ...
```

### 6.3. Variables de Entorno

```bash
# .env.example
SECRET_KEY=cambia_esta_clave_en_produccion
DATABASE_URL=mysql+pymysql://user:password@host:3306/polleria_db
DATABASE_URL_DEV=mysql+pymysql://root:root@localhost:3306/polleria_dev
FLASK_ENV=development
CORS_ORIGINS=http://localhost:5173,https://polleria-frontend.vercel.app
```

---

## 7. ESTRATEGIA DE PRUEBAS

### 7.1. Arquitectura de Pruebas (pytest)

```
tests/
├── conftest.py              ← Fixtures compartidos
│   # app fixture: crea app con config "testing" (SQLite en memoria)
│   # client fixture: Flask test client
│   # db fixture: crea y destruye tablas por test
│   # tokens fixture: genera JWT de prueba por rol
│
├── unit/                    ← Pruebas de la capa Services (SIN HTTP)
│   ├── test_auth_service.py         → autenticar_usuario, hash, verificar
│   ├── test_reserva_service.py      → asignar_mesa, crear_reserva, cancelar
│   ├── test_mesa_service.py         → validar_disponibilidad
│   ├── test_carta_service.py        → CRUD categorías y platillos
│   └── test_takeaway_service.py     → calcular_total, estados, cancelar
│
└── integration/             ← Pruebas de endpoints HTTP completos
    ├── test_auth_routes.py
    ├── test_reservas_routes.py
    ├── test_takeaway_routes.py
    └── test_carta_routes.py
```

### 7.2. Fixture Base (conftest.py)

```python
# tests/conftest.py
import pytest
from app import create_app
from app.extensions import db as _db
from app.models.usuario import Usuario
from flask_jwt_extended import create_access_token

@pytest.fixture(scope="function")
def app():
    app = create_app("testing")
    with app.app_context():
        _db.create_all()
        yield app
        _db.session.remove()
        _db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def token_admin(app):
    with app.app_context():
        return create_access_token(
            identity=1,
            additional_claims={"rol": "ADMIN", "email": "admin@test.com"}
        )

@pytest.fixture
def token_recepcionista(app):
    with app.app_context():
        return create_access_token(
            identity=2,
            additional_claims={"rol": "RECEPCIONISTA", "email": "recep@test.com"}
        )
```

### 7.3. Ejemplo de Prueba Unitaria (capa Services)

```python
# tests/unit/test_reserva_service.py
import pytest
from app.services.reserva_service import asignar_mesa_automatica
from app.models.mesa import Mesa

def test_asignar_mesa_familiar_exitoso(app):
    """RN-02, RN-03: Debe asignar mesa familiar con capacidad ≥ 4"""
    with app.app_context():
        # Arrange: insertar mesa familiar con capacidad 6
        mesa = Mesa(numero=1, capacidad=6, tipo_ocasion="familiar", activo=True)
        _db.session.add(mesa)
        _db.session.commit()

        # Act
        resultado = asignar_mesa_automatica("2026-07-01", "19:00", 4, "familiar")

        # Assert
        assert resultado is not None
        assert resultado.tipo_ocasion == "familiar"
        assert resultado.capacidad >= 4

def test_asignar_mesa_sin_disponibilidad(app):
    """RN-04: Sin mesa disponible debe retornar None"""
    with app.app_context():
        resultado = asignar_mesa_automatica("2026-07-01", "19:00", 4, "familiar")
        assert resultado is None
```

### 7.4. Ejemplo de Prueba de Integración (endpoints)

```python
# tests/integration/test_auth_routes.py
def test_login_exitoso(client):
    """CU-02: Login con credenciales válidas retorna JWT"""
    # Arrange: crear usuario en BD de prueba
    response = client.post("/api/auth/login", json={
        "email": "admin@polleria.com",
        "password": "password123"
    })
    assert response.status_code == 200
    assert "access_token" in response.json

def test_login_credenciales_invalidas(client):
    """CU-02 Alterno A: Login fallido retorna 401"""
    response = client.post("/api/auth/login", json={
        "email": "noexiste@polleria.com",
        "password": "wrongpass"
    })
    assert response.status_code == 401
    assert "error" in response.json

def test_ruta_admin_sin_token(client):
    """RNF-03: Ruta protegida sin JWT retorna 401"""
    response = client.get("/api/usuarios")
    assert response.status_code == 401

def test_ruta_admin_con_rol_recepcionista(client, token_recepcionista):
    """RF-29: Recepcionista no puede acceder a ruta exclusiva de Admin"""
    response = client.get("/api/usuarios", headers={
        "Authorization": f"Bearer {token_recepcionista}"
    })
    assert response.status_code == 403
```

### 7.5. Ejecución y Cobertura

```bash
# Ejecutar todas las pruebas con reporte de cobertura
pytest tests/ --cov=app/services --cov-report=term-missing --cov-report=html -v

# Ejecutar solo pruebas unitarias
pytest tests/unit/ -v

# Ejecutar solo pruebas de integración
pytest tests/integration/ -v

# Verificar que la cobertura supera el 90%
pytest --cov=app/services --cov-fail-under=90
```

**Meta de cobertura:**
```
app/services/auth_service.py        ≥ 90%
app/services/reserva_service.py     ≥ 90%
app/services/mesa_service.py        ≥ 90%
app/services/carta_service.py       ≥ 90%
app/services/takeaway_service.py    ≥ 90%
─────────────────────────────────────────
TOTAL app/services/                 ≥ 90%
```

---

## 8. INTEGRACIÓN CONTINUA (GitHub Actions)

```yaml
# .github/workflows/ci.yml
name: CI — Pruebas y Cobertura

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Configurar Python 3.11
        uses: actions/setup-python@v5
        with:
          python-version: "3.11"

      - name: Instalar dependencias
        run: |
          cd backend
          pip install -r requirements.txt

      - name: Ejecutar pruebas con cobertura
        run: |
          cd backend
          pytest tests/ --cov=app/services --cov-fail-under=90 -v

      - name: Publicar reporte de cobertura
        uses: codecov/codecov-action@v4
        with:
          file: ./backend/coverage.xml
```

---

## 9. DESPLIEGUE

### 9.1. Backend — Render / Railway

```bash
# Procfile (para Render)
web: gunicorn "app:create_app('production')" --bind 0.0.0.0:$PORT

# requirements.txt (dependencias de producción)
Flask==3.1.0
Flask-SQLAlchemy==3.1.1
Flask-JWT-Extended==4.7.1
marshmallow==3.22.0
PyMySQL==1.1.1
bcrypt==4.2.1
flask-cors==5.0.0
gunicorn==23.0.0
python-dotenv==1.0.1
```

**Variables de entorno en Render/Railway:**
```
SECRET_KEY         = <generada con secrets.token_hex(32)>
DATABASE_URL       = <MySQL connection string del proveedor>
FLASK_ENV          = production
CORS_ORIGINS       = https://polleria-frontend.vercel.app
```

### 9.2. Frontend — Vercel

```bash
# Comandos de build
Build Command:  npm run build
Output Dir:     dist
Install Cmd:    npm install
```

**Variables de entorno en Vercel:**
```
VITE_API_URL = https://api.polleria-lenacarbon.onrender.com/api
```

### 9.3. Base de Datos — Railway MySQL

```
Motor:      MySQL 8.x (InnoDB)
Charset:    utf8mb4
Collation:  utf8mb4_unicode_ci
```

---

## 10. FORMATO ESTÁNDAR DE RESPUESTAS API

### Respuesta exitosa
```json
// HTTP 200 / 201
{
  "data": { ... },
  "message": "Operación realizada correctamente"
}
```

### Respuesta de error
```json
// HTTP 400 / 401 / 403 / 404 / 409 / 422
{
  "error": "Descripción del error en español",
  "campo": "nombre_campo_con_error"  // opcional, para errores de validación
}
```

### Respuesta de validación (múltiples errores)
```json
// HTTP 400
{
  "error": "Datos inválidos",
  "detalles": {
    "fecha": ["Este campo es obligatorio."],
    "num_personas": ["Debe ser un número entre 1 y 20."]
  }
}
```

---

## 11. DECISIONES DE ARQUITECTURA (ADR)

| # | Decisión | Alternativa descartada | Justificación |
|---|----------|------------------------|---------------|
| ADR-01 | Backend Flask + Frontend React desacoplados | Monolito Flask + Jinja2 | Permite escalar frontend e independientemente; la API puede reutilizarse en apps móviles futuras. |
| ADR-02 | SQLite en memoria para tests unitarios | MySQL de prueba | Mayor velocidad de ejecución; aislamiento total entre tests; sin dependencia de infraestructura externa en CI. |
| ADR-03 | Tres capas Routes/Services/Models en backend | MVC tradicional | La capa Services es independiente de Flask, lo que permite pruebas unitarias sin contexto HTTP, facilitando el objetivo de 90% de cobertura. |
| ADR-04 | Zustand para estado global en frontend | Redux / Context API | Menor boilerplate; API más simple; suficiente para el alcance del proyecto. |
| ADR-05 | React Hook Form + Zod para formularios | Formik + Yup | Mejor rendimiento (menos re-renders); Zod es más moderno y tiene mejor integración con TypeScript si el proyecto escala. |
| ADR-06 | JWT con expiración configurable desde BD | Expiración fija en código | Permite al Administrador ajustar la seguridad sin redesplegar el backend (tabla Configuracion). |

---

## 12. HISTORIAL DE VERSIONES

| Versión | Fecha | Descripción |
|---------|-------|-------------|
| 1.0.0 | Junio 2026 | Versión inicial — especificación completa de arquitectura SDD |

---

*Documento generado como parte de la metodología Spec Driven Development (SDD) para el proyecto académico IS-489 — UNSCH 2026. Este archivo define la arquitectura técnica que guía la generación de código mediante Inteligencia Artificial en las fases de implementación del proyecto.*
