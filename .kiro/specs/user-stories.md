# user-stories.md
# Sistema Integral de Gestión para Pollería Leña y Carbón
**Historias de Usuario y Product Backlog — Spec Driven Development (SDD)**
**Curso:** IS-489 Pruebas y Aseguramiento de Calidad — UNSCH 2026
**Versión:** 1.0.0 | **Fecha:** Junio 2026

---

## 1. ROLES SCRUM DEL PROYECTO

| Rol | Responsable | Descripción |
|-----|-------------|-------------|
| **Product Owner** | Investigador principal | Define y prioriza los requerimientos del negocio. Representa los intereses del restaurante y sus usuarios (cliente, recepcionista, administrador). |
| **Scrum Master** | Investigador principal | Vela por la correcta aplicación del marco Scrum, organiza los sprints y gestiona los impedimentos técnicos. |
| **Development Team** | Investigador principal (IA asistida — SDD) | Responsable de la arquitectura, diseño UI/UX y codificación full-stack. El código es generado mediante IA a partir de las especificaciones SDD (`.kiro/specs/`). |

> **Enfoque SDD:** A diferencia del desarrollo tradicional, la codificación no es manual. Las especificaciones formalizadas en `requirements.md`, `architecture.md` y `database.md` actúan como prompts estructurados que guían a la IA para generar el código de cada tarea técnica. El rol del desarrollador es supervisar, validar y ajustar el output generado.

---

## 2. ÉPICAS DEL SISTEMA

| Código | Épica | Módulo asociado | Historias |
|--------|-------|-----------------|-----------|
| EP-01 | Gestión de Identidad y Acceso | Usuarios y Roles | HU-01, HU-02, HU-03, HU-04 |
| EP-02 | Gestión de Reservas | Reservas | HU-05, HU-06, HU-07, HU-08 |
| EP-03 | Carta Digital | Carta Digital | HU-09, HU-10, HU-11 |
| EP-04 | Pedidos Takeaway | Takeaway | HU-12, HU-13, HU-14 |
| EP-05 | Panel de Administración | Panel Admin | HU-15, HU-16, HU-17 |

---

## 3. PRODUCT BACKLOG INICIAL

Estimación con técnica **Planning Poker** basada en la sucesión de Fibonacci (1, 2, 3, 5, 8, 13). Los puntos representan esfuerzo, complejidad técnica e incertidumbre.

| Orden | ID | Historia de Usuario | Épica | Prioridad | Puntos | Sprint |
|-------|----|---------------------|-------|-----------|--------|--------|
| 1 | HU-01 | Configuración base del proyecto y BD | EP-01 | Alta | 5 | S1 |
| 2 | HU-02 | Iniciar sesión (Login JWT) | EP-01 | Alta | 3 | S1 |
| 3 | HU-03 | Gestionar usuarios (CRUD Admin) | EP-01 | Alta | 5 | S1 |
| 4 | HU-04 | Cambiar contraseña | EP-01 | Media | 2 | S1 |
| 5 | HU-05 | Registrar reserva con asignación automática de mesa | EP-02 | Alta | 8 | S2 |
| 6 | HU-06 | Consultar disponibilidad de mesas | EP-02 | Alta | 3 | S2 |
| 7 | HU-07 | Listar y actualizar estado de reservas (recepcionista) | EP-02 | Alta | 5 | S2 |
| 8 | HU-08 | Cancelar reserva (cliente con código) | EP-02 | Media | 3 | S2 |
| 9 | HU-09 | Visualizar carta digital pública | EP-03 | Alta | 3 | S3 |
| 10 | HU-10 | Gestionar categorías de la carta | EP-03 | Alta | 3 | S3 |
| 11 | HU-11 | Gestionar platillos de la carta | EP-03 | Alta | 5 | S3 |
| 12 | HU-12 | Realizar pedido takeaway | EP-04 | Alta | 8 | S4 |
| 13 | HU-13 | Consultar estado del pedido (cliente) | EP-04 | Alta | 2 | S4 |
| 14 | HU-14 | Listar y actualizar estado de pedidos (recepcionista) | EP-04 | Alta | 5 | S4 |
| 15 | HU-15 | Dashboard de administración | EP-05 | Media | 5 | S4 |
| 16 | HU-16 | Gestionar mesas | EP-05 | Media | 3 | S4 |
| 17 | HU-17 | Gestionar configuración del sistema | EP-05 | Baja | 3 | S4 |

**Total puntos de historia: 71**

### Distribución por prioridad
| Prioridad | Puntos | % |
|-----------|--------|---|
| Alta | 55 | 77% |
| Media | 13 | 18% |
| Baja | 3 | 4% |

---

## 4. PLANIFICACIÓN DE SPRINTS

| Sprint | Nombre | Duración | Objetivo | Puntos | HU incluidas |
|--------|--------|----------|----------|--------|--------------|
| Sprint 1 | Fundamentos y Seguridad | 2 semanas | Establecer la base técnica, autenticación JWT y gestión de usuarios | 15 | HU-01..HU-04 |
| Sprint 2 | Motor de Reservas | 2 semanas | Implementar el módulo de reservas con asignación automática de mesas | 19 | HU-05..HU-08 |
| Sprint 3 | Carta Digital | 2 semanas | Implementar la carta pública y su gestión desde el panel admin | 11 | HU-09..HU-11 |
| Sprint 4 | Takeaway y Panel Admin | 2 semanas | Completar pedidos takeaway, dashboard y configuración del sistema | 26 | HU-12..HU-17 |

---

## 5. HISTORIAS DE USUARIO — DETALLE COMPLETO

---

### SPRINT 1 — Fundamentos y Seguridad
**Objetivo:** Establecer la arquitectura base, configurar el entorno de desarrollo, la base de datos MySQL y el sistema de autenticación JWT. Sin esta base, ningún otro módulo puede operar de forma segura.
**Capacidad del sprint:** 15 puntos de historia

---

#### HU-01 — Configuración base del proyecto y base de datos

| Campo | Detalle |
|-------|---------|
| **ID** | HU-01 |
| **Épica** | EP-01 — Gestión de Identidad y Acceso |
| **Prioridad** | Alta |
| **Estimación** | 5 puntos / aprox. 8 horas ideales |
| **Sprint** | Sprint 1 |

**Historia:**
> Como **equipo de desarrollo**,
> quiero **configurar el repositorio GitHub, la estructura de carpetas SDD, el entorno Flask y la base de datos MySQL con todas las tablas**,
> para que **el proyecto tenga una base técnica sólida y reproducible desde la que generar el resto de módulos con IA**.

**Criterios de Aceptación:**
1. El repositorio en GitHub tiene la estructura de carpetas definida en `architecture.md` (`backend/`, `frontend/`, `tests/`, `.kiro/specs/`).
2. La base de datos MySQL contiene las 8 tablas con sus relaciones, constraints e índices según `database.md`.
3. El comando `flask run` levanta el servidor en `http://localhost:5000` sin errores.
4. El comando `npm run dev` levanta el frontend en `http://localhost:5173` sin errores.
5. El endpoint `GET /api/health` retorna `{"status": "ok"}` con HTTP 200.
6. El archivo `.env.example` documenta todas las variables de entorno necesarias.
7. El workflow de GitHub Actions ejecuta `pytest` exitosamente en cada push a `main`.

**Desglose de Tareas Técnicas:**

| ID | Capa | Tarea | Prompt SDD para IA |
|----|------|-------|--------------------|
| T1 | BD | Crear script DDL completo en MySQL con las 8 tablas, FK, índices y datos semilla de `Configuracion` | Usar `database.md` como especificación |
| T2 | Backend | Inicializar proyecto Flask con Application Factory, extensiones (db, jwt, ma, cors) y Blueprints vacíos | Usar `architecture.md` sección 2.3 |
| T3 | Backend | Configurar `config.py` con tres entornos (dev, testing, production) y SQLite en memoria para tests | Usar `architecture.md` sección 2.4 |
| T4 | Backend | Crear endpoint `GET /api/health` y `conftest.py` con fixtures base para pytest | Usar `architecture.md` sección 7.2 |
| T5 | Frontend | Inicializar proyecto React + Vite + Tailwind CSS + shadcn/ui + React Router v6 | Usar `architecture.md` sección 4.1 |
| T6 | Frontend | Crear instancia Axios con interceptor JWT y store Zustand de autenticación | Usar `architecture.md` secciones 4.3 y 4.4 |
| T7 | CI/CD | Crear `.github/workflows/ci.yml` con job de pytest y verificación de cobertura ≥ 90% | Usar `architecture.md` sección 8 |

---

#### HU-02 — Iniciar sesión (Login JWT)

| Campo | Detalle |
|-------|---------|
| **ID** | HU-02 |
| **Épica** | EP-01 — Gestión de Identidad y Acceso |
| **Prioridad** | Alta |
| **Estimación** | 3 puntos / aprox. 5 horas ideales |
| **Sprint** | Sprint 1 |
| **RF asociado** | RF-25, RF-26 |

**Historia:**
> Como **recepcionista o administrador**,
> quiero **ingresar mi correo y contraseña en un formulario de login**,
> para que **el sistema valide mis credenciales, genere un token JWT y me dé acceso a las funcionalidades de mi rol**.

**Criterios de Aceptación:**
1. `POST /api/auth/login` con credenciales válidas retorna HTTP 200 con `{access_token, usuario:{id, nombre, email, rol}}`.
2. Con credenciales inválidas retorna HTTP 401 con `{"error": "Credenciales inválidas"}`.
3. Con cuenta desactivada retorna HTTP 403 con `{"error": "Cuenta desactivada"}`.
4. La contraseña se verifica con `bcrypt.checkpw()` contra el hash almacenado.
5. El JWT incluye en su payload: `user_id`, `email`, `rol` y `exp`.
6. `POST /api/auth/logout` con token válido retorna HTTP 200.
7. El formulario React deshabilita el botón "Ingresar" y muestra un spinner mientras carga.
8. Tras login exitoso, el token se guarda en Zustand y localStorage, y se redirige según rol.

**Desglose de Tareas Técnicas:**

| ID | Capa | Tarea | Prompt SDD para IA |
|----|------|-------|--------------------|
| T1 | Backend | Crear `auth_service.py` con función `autenticar_usuario(email, password)` que verifica bcrypt y retorna datos del usuario o None | Basado en RF-25, RN-07 |
| T2 | Backend | Crear `auth_routes.py` con `POST /api/auth/login` que usa el servicio y genera JWT con `create_access_token` | Basado en `architecture.md` endpoint #1 |
| T3 | Backend | Implementar `POST /api/auth/logout` con lista negra de tokens (blocklist en memoria o BD) | Basado en RF-26 |
| T4 | Backend | Crear schema Marshmallow `LoginSchema` para validar `email` y `password` | Basado en `architecture.md` sección 2.1 |
| T5 | Tests | Escribir `test_auth_service.py`: casos login exitoso, password incorrecto, cuenta inactiva, email inexistente | Cobertura función crítica #3 |
| T6 | Tests | Escribir `test_auth_routes.py`: login 200, 401, 403; logout 200 | Cobertura integración |
| T7 | Frontend | Crear `LoginPage.jsx` con React Hook Form + Zod, integración Axios y manejo de errores | RF-25 |
| T8 | Frontend | Actualizar `authStore.js` para persistir token y datos del usuario tras login exitoso | `architecture.md` sección 4.3 |

---

#### HU-03 — Gestionar usuarios (CRUD Administrador)

| Campo | Detalle |
|-------|---------|
| **ID** | HU-03 |
| **Épica** | EP-01 — Gestión de Identidad y Acceso |
| **Prioridad** | Alta |
| **Estimación** | 5 puntos / aprox. 8 horas ideales |
| **Sprint** | Sprint 1 |
| **RF asociado** | RF-27, RF-29 |

**Historia:**
> Como **administrador**,
> quiero **crear, editar, activar y desactivar cuentas de usuarios del sistema**,
> para que **solo las personas autorizadas puedan acceder al panel de operaciones del restaurante**.

**Criterios de Aceptación:**
1. `GET /api/usuarios` (solo ADMIN) retorna lista de todos los usuarios con HTTP 200.
2. `POST /api/usuarios` crea un usuario con contraseña hasheada (bcrypt, 12 rounds); retorna HTTP 201.
3. Crear usuario con email duplicado retorna HTTP 409.
4. `PUT /api/usuarios/:id` actualiza nombre, email o rol; retorna HTTP 200.
5. `PATCH /api/usuarios/:id/estado` activa o desactiva la cuenta; retorna HTTP 200.
6. Acceder a cualquier endpoint de este módulo sin rol ADMIN retorna HTTP 403.
7. La tabla de usuarios en el panel React muestra nombre, email, rol y estado (badge de color).
8. El formulario de creación valida que el rol sea solo `RECEPCIONISTA` o `ADMIN` (el rol CLIENTE no se crea).

**Desglose de Tareas Técnicas:**

| ID | Capa | Tarea | Prompt SDD para IA |
|----|------|-------|--------------------|
| T1 | Backend | Crear modelo `Usuario` en SQLAlchemy con campos según `database.md`; método `set_password()` con bcrypt | Basado en entidad Usuario |
| T2 | Backend | Crear `usuarios_routes.py` con los 5 endpoints del módulo USUARIOS y decorador `@rol_requerido("ADMIN")` | `architecture.md` endpoints #5..#9 |
| T3 | Backend | Crear schema `UsuarioSchema` con validación de email único, rol válido y contraseña mínimo 8 caracteres | RF-27, RN-07 |
| T4 | Tests | Escribir `test_usuarios_routes.py`: CRUD completo, 403 sin rol admin, 409 email duplicado | Cobertura integración |
| T5 | Frontend | Crear `UsuariosPage.jsx` con tabla de datos shadcn/ui, modal de creación/edición y toggle de estado | RF-27 |

---

#### HU-04 — Cambiar contraseña

| Campo | Detalle |
|-------|---------|
| **ID** | HU-04 |
| **Épica** | EP-01 — Gestión de Identidad y Acceso |
| **Prioridad** | Media |
| **Estimación** | 2 puntos / aprox. 3 horas ideales |
| **Sprint** | Sprint 1 |
| **RF asociado** | RF-28 |

**Historia:**
> Como **recepcionista o administrador autenticado**,
> quiero **cambiar mi contraseña ingresando la contraseña actual y la nueva**,
> para que **pueda mantener la seguridad de mi cuenta**.

**Criterios de Aceptación:**
1. `PUT /api/auth/cambiar-password` con token válido, contraseña actual correcta y nueva contraseña retorna HTTP 200.
2. Si la contraseña actual no coincide, retorna HTTP 400 con `{"error": "Contraseña actual incorrecta"}`.
3. La nueva contraseña se hashea con bcrypt antes de guardarse.
4. La nueva contraseña debe tener mínimo 8 caracteres; si no, retorna HTTP 400.
5. El formulario React muestra/oculta la contraseña con un toggle de visibilidad.

**Desglose de Tareas Técnicas:**

| ID | Capa | Tarea | Prompt SDD para IA |
|----|------|-------|--------------------|
| T1 | Backend | Agregar función `cambiar_password(user_id, pwd_actual, pwd_nueva)` en `auth_service.py` | RF-28 |
| T2 | Backend | Crear endpoint `PUT /api/auth/cambiar-password` con `@jwt_required()` | `architecture.md` endpoint #3 |
| T3 | Tests | Agregar casos en `test_auth_service.py`: cambio exitoso, pwd actual incorrecto, nueva pwd muy corta | Cobertura función crítica #3 |
| T4 | Frontend | Crear componente `CambiarPasswordForm.jsx` con React Hook Form + Zod y toggle de visibilidad | RF-28 |

---

### SPRINT 2 — Motor de Reservas
**Objetivo:** Implementar el módulo central de Reservas, incluyendo la lógica de asignación automática de mesas por tipo de ocasión, que es la funcionalidad más compleja del sistema y de mayor valor para el negocio.
**Capacidad del sprint:** 19 puntos de historia

---

#### HU-05 — Registrar reserva con asignación automática de mesa

| Campo | Detalle |
|-------|---------|
| **ID** | HU-05 |
| **Épica** | EP-02 — Gestión de Reservas |
| **Prioridad** | Alta |
| **Estimación** | 8 puntos / aprox. 13 horas ideales |
| **Sprint** | Sprint 2 |
| **RF asociado** | RF-01, RF-02, RF-04 |

**Historia:**
> Como **cliente**,
> quiero **registrar una reserva indicando mi nombre, la fecha, hora, número de personas y tipo de ocasión**,
> para que **el sistema asigne automáticamente la mesa más adecuada y me entregue un código de confirmación**.

**Criterios de Aceptación:**
1. `POST /api/reservas` con datos válidos retorna HTTP 201 con `{id, codigo_confirmacion, mesa:{numero}, fecha, hora, estado:"pendiente"}`.
2. La mesa se asigna automáticamente sin intervención del recepcionista (RN-01, RN-02, RN-03).
3. Si no hay mesa disponible, retorna HTTP 409 con `{"error": "No hay mesas disponibles para el horario y tipo de ocasión seleccionados"}`.
4. El `codigo_confirmacion` es único y tiene formato alfanumérico de 8 caracteres (ej. `POLL-A1B2`).
5. Fecha pasada retorna HTTP 400.
6. Campos faltantes u obligatorios vacíos retornan HTTP 400 con detalle de campos inválidos.
7. El formulario React valida todos los campos con Zod antes de enviar la petición.
8. Tras la creación exitosa, la UI muestra el código de confirmación en pantalla de forma destacada.

**Reglas de negocio aplicadas:**
- **RN-01:** Bloqueo de 2 horas por mesa reservada.
- **RN-02:** Prioridad: disponibilidad → tipo_ocasion → capacidad mínima.
- **RN-03:** familiar ≥ 4 personas; romántica = 2 personas; reunión ≥ 6 personas.
- **RN-04:** Sin mesa válida → HTTP 409, no se crea la reserva.

**Desglose de Tareas Técnicas:**

| ID | Capa | Tarea | Prompt SDD para IA |
|----|------|-------|--------------------|
| T1 | BD | Crear modelos `Mesa` y `Reserva` en SQLAlchemy con todos los campos y relación FK | `database.md` entidades Mesa y Reserva |
| T2 | Backend | Crear función `validar_disponibilidad_mesa(mesa_id, fecha, hora)` en `mesa_service.py` — detecta conflictos de bloqueo de 2 horas | RN-01, función crítica #7 |
| T3 | Backend | Crear función `asignar_mesa_automatica(fecha, hora, personas, tipo_ocasion)` en `reserva_service.py` — aplica RN-01..RN-04 | RN-02, RN-03, RN-04, función crítica #1 |
| T4 | Backend | Crear función `crear_reserva(datos)` en `reserva_service.py` — llama al asignador y persiste la reserva con código único | RF-01, RF-04, función crítica #2 |
| T5 | Backend | Crear `reservas_routes.py` con `POST /api/reservas` (público) y schema Marshmallow de validación | `architecture.md` endpoint #14 |
| T6 | Tests | Escribir `test_reserva_service.py`: asignación exitosa por tipo, sin disponibilidad, bloqueo de horario, código único | Funciones críticas #1, #2, #7 |
| T7 | Tests | Escribir `test_reservas_routes.py`: HTTP 201, 409, 400 campos faltantes, 400 fecha pasada | Cobertura integración |
| T8 | Frontend | Crear `ReservaPage.jsx` con formulario de 5 campos, selector de tipo de ocasión y pantalla de confirmación con código | RF-01 |

---

#### HU-06 — Consultar disponibilidad de mesas

| Campo | Detalle |
|-------|---------|
| **ID** | HU-06 |
| **Épica** | EP-02 — Gestión de Reservas |
| **Prioridad** | Alta |
| **Estimación** | 3 puntos / aprox. 5 horas ideales |
| **Sprint** | Sprint 2 |
| **RF asociado** | RF-03 |

**Historia:**
> Como **cliente**,
> quiero **consultar si hay disponibilidad antes de confirmar mi reserva**,
> para que **no pierda tiempo llenando el formulario si no hay mesas disponibles en mi horario deseado**.

**Criterios de Aceptación:**
1. `GET /api/reservas/disponibilidad?fecha=&hora=&tipo_ocasion=&num_personas=` retorna HTTP 200 con `{disponible: true/false}`.
2. Si hay disponibilidad, la respuesta incluye `horarios_sugeridos` con hasta 3 alternativas cercanas.
3. Si `disponible: false`, la UI muestra mensaje claro: "No hay mesas disponibles. Prueba otro horario."
4. El componente React consulta la disponibilidad en tiempo real al cambiar fecha, hora o tipo de ocasión (debounce de 500ms).

**Desglose de Tareas Técnicas:**

| ID | Capa | Tarea | Prompt SDD para IA |
|----|------|-------|--------------------|
| T1 | Backend | Crear función `consultar_disponibilidad(fecha, hora, tipo_ocasion, num_personas)` en `reserva_service.py` | RF-03 |
| T2 | Backend | Crear endpoint `GET /api/reservas/disponibilidad` (público) | `architecture.md` endpoint #15 |
| T3 | Tests | Agregar casos en `test_reserva_service.py`: disponible, no disponible, horarios alternativos | Cobertura |
| T4 | Frontend | Agregar consulta de disponibilidad con debounce en `ReservaPage.jsx` | RF-03 |

---

#### HU-07 — Listar y actualizar estado de reservas (recepcionista)

| Campo | Detalle |
|-------|---------|
| **ID** | HU-07 |
| **Épica** | EP-02 — Gestión de Reservas |
| **Prioridad** | Alta |
| **Estimación** | 5 puntos / aprox. 8 horas ideales |
| **Sprint** | Sprint 2 |
| **RF asociado** | RF-05, RF-06, RF-08 |

**Historia:**
> Como **recepcionista**,
> quiero **ver todas las reservas del día con su estado y poder actualizarlas (confirmar, completar, cancelar)**,
> para que **pueda gestionar la operación diaria del restaurante de forma eficiente**.

**Criterios de Aceptación:**
1. `GET /api/reservas?fecha=hoy` retorna todas las reservas del día con HTTP 200 (requiere token RECEPCIONISTA o ADMIN).
2. `PATCH /api/reservas/:id/estado` actualiza el estado con las transiciones válidas (pendiente→confirmada, confirmada→completada, cualquiera→cancelada).
3. Una transición de estado inválida retorna HTTP 422.
4. La vista React muestra reservas en tarjetas organizadas por hora, con badge de color por estado.
5. Los botones de acción (Confirmar / Completar / Cancelar) se muestran condicionalmente según el estado actual.
6. La lista se actualiza automáticamente al cambiar un estado (sin recargar la página).

**Desglose de Tareas Técnicas:**

| ID | Capa | Tarea | Prompt SDD para IA |
|----|------|-------|--------------------|
| T1 | Backend | Crear función `listar_reservas(fecha, estado)` en `reserva_service.py` | RF-05 |
| T2 | Backend | Crear función `actualizar_estado_reserva(reserva_id, nuevo_estado)` con validación de transiciones | RF-06 |
| T3 | Backend | Crear endpoints `GET /api/reservas` y `PATCH /api/reservas/:id/estado` con `@rol_requerido("RECEPCIONISTA","ADMIN")` | `architecture.md` endpoints #16, #18 |
| T4 | Tests | Agregar casos de transición de estado válida e inválida en `test_reserva_service.py` | Cobertura |
| T5 | Frontend | Crear `ReservasDiaPage.jsx` con lista de tarjetas de reserva, filtro por estado y botones de acción condicionales | RF-05, RF-06 |

---

#### HU-08 — Cancelar reserva (cliente con código de confirmación)

| Campo | Detalle |
|-------|---------|
| **ID** | HU-08 |
| **Épica** | EP-02 — Gestión de Reservas |
| **Prioridad** | Media |
| **Estimación** | 3 puntos / aprox. 5 horas ideales |
| **Sprint** | Sprint 2 |
| **RF asociado** | RF-07 |

**Historia:**
> Como **cliente**,
> quiero **cancelar mi reserva ingresando el código de confirmación que recibí**,
> para que **la mesa quede disponible para otras personas si ya no podré asistir**.

**Criterios de Aceptación:**
1. `POST /api/reservas/cancelar` con `{codigo_confirmacion}` válido y con más de 1 hora de anticipación retorna HTTP 200.
2. Código inexistente retorna HTTP 404 con `{"error": "Reserva no encontrada"}`.
3. Cancelación con menos de 1 hora de anticipación retorna HTTP 422 con mensaje explicativo.
4. Reserva ya cancelada o completada retorna HTTP 422.
5. La UI tiene un campo de texto para ingresar el código y muestra el resultado claramente.

**Desglose de Tareas Técnicas:**

| ID | Capa | Tarea | Prompt SDD para IA |
|----|------|-------|--------------------|
| T1 | Backend | Crear función `cancelar_reserva_por_codigo(codigo)` en `reserva_service.py` con validación de plazo de 1 hora | RF-07 |
| T2 | Backend | Crear endpoint público `POST /api/reservas/cancelar` | `architecture.md` endpoint #19 |
| T3 | Tests | Agregar casos: cancelación exitosa, código inválido, fuera de plazo, ya cancelada | Cobertura |
| T4 | Frontend | Agregar sección "Cancelar mi reserva" en `ReservaPage.jsx` con campo de código | RF-07 |

---

### SPRINT 3 — Carta Digital
**Objetivo:** Implementar la carta digital pública y las herramientas de gestión de menú para el administrador (categorías y platillos).
**Capacidad del sprint:** 11 puntos de historia

---

#### HU-09 — Visualizar carta digital pública

| Campo | Detalle |
|-------|---------|
| **ID** | HU-09 |
| **Épica** | EP-03 — Carta Digital |
| **Prioridad** | Alta |
| **Estimación** | 3 puntos / aprox. 5 horas ideales |
| **Sprint** | Sprint 3 |
| **RF asociado** | RF-09, RF-10 |

**Historia:**
> Como **cliente**,
> quiero **ver la carta digital del restaurante organizada por categorías, con foto, nombre y precio de cada platillo**,
> para que **pueda revisar el menú antes de llegar o al momento de hacer mi pedido**.

**Criterios de Aceptación:**
1. `GET /api/categorias` retorna categorías activas con sus platillos activos anidados (HTTP 200, sin autenticación).
2. `GET /api/platillos?categoria_id=X` filtra platillos por categoría (HTTP 200).
3. Solo los platillos con `activo=true` aparecen en la carta pública.
4. La UI React muestra la carta con tabs o acordeón por categoría.
5. Cada platillo muestra: imagen (o placeholder si no tiene), nombre, descripción y precio en soles (S/).
6. La vista es completamente responsiva (móvil y escritorio).

**Desglose de Tareas Técnicas:**

| ID | Capa | Tarea | Prompt SDD para IA |
|----|------|-------|--------------------|
| T1 | BD | Crear modelos `Categoria` y `Platillo` en SQLAlchemy con relación FK y campo `activo` | `database.md` entidades Categoria y Platillo |
| T2 | Backend | Crear función `listar_carta_publica()` en `carta_service.py` que retorna categorías con platillos activos anidados | RF-09 |
| T3 | Backend | Crear `carta_routes.py` con `GET /api/categorias` y `GET /api/platillos` (públicos) | `architecture.md` endpoints #20, #24 |
| T4 | Tests | Escribir `test_carta_service.py`: carta con platillos activos, platillos desactivados no aparecen, filtro por categoría | Cobertura función crítica #8 |
| T5 | Frontend | Crear `HomePage.jsx` con grilla de categorías y tarjetas de platillos, placeholder de imagen, precio formateado | RF-09, RF-10 |

---

#### HU-10 — Gestionar categorías de la carta

| Campo | Detalle |
|-------|---------|
| **ID** | HU-10 |
| **Épica** | EP-03 — Carta Digital |
| **Prioridad** | Alta |
| **Estimación** | 3 puntos / aprox. 5 horas ideales |
| **Sprint** | Sprint 3 |
| **RF asociado** | RF-11, RF-13 |

**Historia:**
> Como **administrador**,
> quiero **crear, editar y eliminar las categorías de la carta digital**,
> para que **la organización del menú refleje siempre la oferta actual del restaurante**.

**Criterios de Aceptación:**
1. `POST /api/categorias` crea una categoría nueva; retorna HTTP 201 (solo ADMIN).
2. `PUT /api/categorias/:id` edita nombre o descripción; retorna HTTP 200.
3. `DELETE /api/categorias/:id` elimina la categoría solo si no tiene platillos activos; retorna HTTP 200.
4. Eliminar categoría con platillos activos retorna HTTP 409 con `{"error": "No se puede eliminar una categoría con platillos activos"}` (RN-09).
5. El panel admin muestra la lista de categorías con conteo de platillos asociados.
6. Formularios de creación y edición validan que el nombre no esté vacío.

**Desglose de Tareas Técnicas:**

| ID | Capa | Tarea | Prompt SDD para IA |
|----|------|-------|--------------------|
| T1 | Backend | Crear funciones CRUD de categorías en `carta_service.py` con validación RN-09 en la eliminación | RF-11, RN-09 |
| T2 | Backend | Agregar endpoints `POST`, `PUT`, `DELETE /api/categorias/:id` con `@rol_requerido("ADMIN")` | `architecture.md` endpoints #21, #22, #23 |
| T3 | Tests | Agregar casos en `test_carta_service.py`: crear, editar, eliminar sin platillos activos, 409 con platillos | RN-09, cobertura |
| T4 | Frontend | Agregar sección de categorías en `CartaPage.jsx` con tabla, modal de formulario y botón de eliminar con confirmación | RF-11 |

---

#### HU-11 — Gestionar platillos de la carta

| Campo | Detalle |
|-------|---------|
| **ID** | HU-11 |
| **Épica** | EP-03 — Carta Digital |
| **Prioridad** | Alta |
| **Estimación** | 5 puntos / aprox. 8 horas ideales |
| **Sprint** | Sprint 3 |
| **RF asociado** | RF-12, RF-13 |

**Historia:**
> Como **administrador**,
> quiero **crear, editar, activar y desactivar platillos de la carta**,
> para que **el menú digital siempre refleje lo que está disponible en el restaurante**.

**Criterios de Aceptación:**
1. `POST /api/platillos` crea un platillo con nombre, descripción, precio, imagen_url y categoría; retorna HTTP 201.
2. `PUT /api/platillos/:id` edita cualquier campo del platillo; retorna HTTP 200.
3. `PATCH /api/platillos/:id/estado` con `{activo: false}` oculta el platillo de la carta pública; retorna HTTP 200.
4. Un platillo desactivado no aparece en `GET /api/categorias` ni en `GET /api/platillos` sin filtro admin.
5. Los registros históricos de pedidos que incluían el platillo se conservan intactos (RN-08).
6. Precio negativo o cero retorna HTTP 400.
7. El panel admin muestra platillos en tabla con badge de estado y toggle activo/inactivo.

**Desglose de Tareas Técnicas:**

| ID | Capa | Tarea | Prompt SDD para IA |
|----|------|-------|--------------------|
| T1 | Backend | Crear funciones CRUD de platillos y `cambiar_visibilidad_platillo()` en `carta_service.py` | RF-12, RF-13, RN-08, función crítica #8 |
| T2 | Backend | Agregar endpoints `POST`, `PUT`, `PATCH /api/platillos/:id/estado` con `@rol_requerido("ADMIN")` | `architecture.md` endpoints #25, #26, #27 |
| T3 | Tests | Agregar en `test_carta_service.py`: crear platillo, editar, activar, desactivar, precio inválido, historial conservado | Cobertura función crítica #8 |
| T4 | Frontend | Completar `CartaPage.jsx` con sección de platillos: tabla, modal de formulario con selector de categoría y toggle de estado | RF-12, RF-13 |

---

### SPRINT 4 — Takeaway y Panel de Administración
**Objetivo:** Completar el módulo de pedidos takeaway con seguimiento para el cliente y para el recepcionista, e implementar el panel de administración con dashboard, gestión de mesas y configuración del sistema.
**Capacidad del sprint:** 26 puntos de historia

---

#### HU-12 — Realizar pedido takeaway

| Campo | Detalle |
|-------|---------|
| **ID** | HU-12 |
| **Épica** | EP-04 — Pedidos Takeaway |
| **Prioridad** | Alta |
| **Estimación** | 8 puntos / aprox. 13 horas ideales |
| **Sprint** | Sprint 4 |
| **RF asociado** | RF-14, RF-15, RF-16 |

**Historia:**
> Como **cliente**,
> quiero **seleccionar platillos de la carta, indicar mi nombre y contacto, y confirmar un pedido para llevar**,
> para que **el restaurante prepare mi pedido y yo pueda recogerlo sin esperar en el local**.

**Criterios de Aceptación:**
1. `POST /api/takeaway` con nombre, contacto y al menos un ítem retorna HTTP 201 con `{id, codigo_seguimiento, total, estado:"recibido", items}`.
2. El `codigo_seguimiento` es único con formato `TW-XXXXXXXX`.
3. El total se calcula como Σ(precio_unitario × cantidad) y se fija al momento de confirmar (RN-06).
4. Si el carrito está vacío, retorna HTTP 400 con `{"error": "El pedido debe contener al menos un platillo"}`.
5. Si un platillo está desactivado, retorna HTTP 422 indicando el platillo no disponible.
6. La UI React tiene un carrito lateral donde el cliente agrega platillos con sus cantidades.
7. El resumen del carrito muestra subtotal por ítem y total final en soles (S/).
8. Tras confirmar, se muestra el código de seguimiento en pantalla de éxito.

**Reglas de negocio aplicadas:**
- **RN-06:** Precio fijado en el momento de confirmación; no cambia si el precio del platillo cambia después.

**Desglose de Tareas Técnicas:**

| ID | Capa | Tarea | Prompt SDD para IA |
|----|------|-------|--------------------|
| T1 | BD | Crear modelos `PedidoTakeaway` y `DetallePedido` en SQLAlchemy con relaciones FK | `database.md` entidades PedidoTakeaway y DetallePedido |
| T2 | Backend | Crear función `calcular_total_pedido(items)` en `takeaway_service.py` | RF-16, RN-06, función crítica #4 |
| T3 | Backend | Crear función `crear_pedido_takeaway(datos)` en `takeaway_service.py` — valida ítems, calcula total, genera código, persiste con transacción | RF-14, RF-15, RF-16, función crítica #5 |
| T4 | Backend | Crear `takeaway_routes.py` con `POST /api/takeaway` (público) y schema Marshmallow de validación | `architecture.md` endpoint #28 |
| T5 | Tests | Escribir `test_takeaway_service.py`: pedido exitoso, carrito vacío, platillo desactivado, cálculo total correcto, código único | Funciones críticas #4 y #5 |
| T6 | Tests | Escribir `test_takeaway_routes.py`: HTTP 201, 400 vacío, 422 platillo inactivo | Cobertura integración |
| T7 | Frontend | Crear `TakeawayPage.jsx` con carta de platillos clickeable, carrito lateral con cantidades, resumen de total y formulario de datos del cliente | RF-14, RF-15 |
| T8 | Frontend | Crear `cartaStore.js` en Zustand para gestionar el estado del carrito (agregar, quitar, vaciar) | `architecture.md` sección 4.1 |

---

#### HU-13 — Consultar estado del pedido (cliente)

| Campo | Detalle |
|-------|---------|
| **ID** | HU-13 |
| **Épica** | EP-04 — Pedidos Takeaway |
| **Prioridad** | Alta |
| **Estimación** | 2 puntos / aprox. 3 horas ideales |
| **Sprint** | Sprint 4 |
| **RF asociado** | RF-19 |

**Historia:**
> Como **cliente**,
> quiero **consultar el estado actual de mi pedido ingresando el código de seguimiento**,
> para que **sepa si mi pedido ya está listo para recoger sin tener que llamar al restaurante**.

**Criterios de Aceptación:**
1. `GET /api/takeaway/estado/:codigo` retorna HTTP 200 con `{codigo_seguimiento, estado, total, items, created_at}` (sin autenticación).
2. Código inexistente retorna HTTP 404 con `{"error": "Pedido no encontrado"}`.
3. La UI tiene un campo de búsqueda por código y muestra el estado con un ícono visual (reloj, fuego, tick, caja).
4. El estado se muestra como barra de progreso: Recibido → En preparación → Listo → Entregado.

**Desglose de Tareas Técnicas:**

| ID | Capa | Tarea | Prompt SDD para IA |
|----|------|-------|--------------------|
| T1 | Backend | Crear función `consultar_pedido_por_codigo(codigo)` en `takeaway_service.py` | RF-19 |
| T2 | Backend | Crear endpoint público `GET /api/takeaway/estado/:codigo` | `architecture.md` endpoint #29 |
| T3 | Tests | Agregar casos: código válido, código inexistente | Cobertura |
| T4 | Frontend | Crear `SeguimientoPage.jsx` con barra de progreso de estados | RF-19 |

---

#### HU-14 — Listar y actualizar estado de pedidos (recepcionista)

| Campo | Detalle |
|-------|---------|
| **ID** | HU-14 |
| **Épica** | EP-04 — Pedidos Takeaway |
| **Prioridad** | Alta |
| **Estimación** | 5 puntos / aprox. 8 horas ideales |
| **Sprint** | Sprint 4 |
| **RF asociado** | RF-17, RF-18, RF-20 |

**Historia:**
> Como **recepcionista**,
> quiero **ver todos los pedidos takeaway activos y actualizar su estado conforme avanzan**,
> para que **pueda coordinar la preparación y entrega de pedidos de forma ordenada**.

**Criterios de Aceptación:**
1. `GET /api/takeaway` retorna pedidos con filtro por fecha y estado (requiere RECEPCIONISTA o ADMIN).
2. `PATCH /api/takeaway/:id/estado` actualiza el estado con las transiciones válidas.
3. Cancelar un pedido en estado "en_preparacion", "listo" o "entregado" retorna HTTP 422 (RN-05).
4. La UI muestra pedidos en tarjetas organizadas por estado con el nombre del cliente y los ítems.
5. Botones de acción condicionales según el estado actual del pedido.

**Desglose de Tareas Técnicas:**

| ID | Capa | Tarea | Prompt SDD para IA |
|----|------|-------|--------------------|
| T1 | Backend | Crear función `actualizar_estado_pedido(pedido_id, nuevo_estado)` en `takeaway_service.py` con validación de transiciones | RF-18, RN-05, función crítica #6 |
| T2 | Backend | Crear endpoints `GET /api/takeaway`, `GET /api/takeaway/:id`, `PATCH /api/takeaway/:id/estado` con `@rol_requerido` | `architecture.md` endpoints #30..#32 |
| T3 | Tests | Agregar casos en `test_takeaway_service.py`: transiciones válidas, cancelar solo desde "recibido" (RN-05), 422 | Función crítica #6 |
| T4 | Frontend | Crear `PedidosDiaPage.jsx` con columnas kanban por estado y botones de transición condicionales | RF-17, RF-18 |

---

#### HU-15 — Dashboard de administración

| Campo | Detalle |
|-------|---------|
| **ID** | HU-15 |
| **Épica** | EP-05 — Panel de Administración |
| **Prioridad** | Media |
| **Estimación** | 5 puntos / aprox. 8 horas ideales |
| **Sprint** | Sprint 4 |
| **RF asociado** | RF-21, RF-23, RF-24 |

**Historia:**
> Como **administrador**,
> quiero **ver un panel con métricas del día: reservas, pedidos takeaway, ingresos estimados y platillos más solicitados**,
> para que **pueda tomar decisiones operativas con información actualizada**.

**Criterios de Aceptación:**
1. `GET /api/admin/dashboard` retorna HTTP 200 con `{reservas_hoy, pedidos_hoy, ingresos_estimados, platillos_top:[{nombre, cantidad}]}`.
2. `GET /api/admin/reservas` permite filtrar reservas por fecha y estado.
3. `GET /api/admin/pedidos` permite filtrar pedidos por fecha y estado.
4. La UI muestra tarjetas KPI con íconos, historial de reservas en tabla y top de platillos en lista.

**Desglose de Tareas Técnicas:**

| ID | Capa | Tarea | Prompt SDD para IA |
|----|------|-------|--------------------|
| T1 | Backend | Crear endpoints en `admin_routes.py`: dashboard, historial de reservas, historial de pedidos con filtros | `architecture.md` endpoints #33..#35 |
| T2 | Frontend | Crear `DashboardPage.jsx` con 4 tarjetas KPI (reservas, pedidos, ingresos, top platillos) | RF-21 |

---

#### HU-16 — Gestionar mesas

| Campo | Detalle |
|-------|---------|
| **ID** | HU-16 |
| **Épica** | EP-05 — Panel de Administración |
| **Prioridad** | Media |
| **Estimación** | 3 puntos / aprox. 5 horas ideales |
| **Sprint** | Sprint 4 |
| **RF asociado** | RF-08 |

**Historia:**
> Como **administrador**,
> quiero **registrar, editar y desactivar las mesas del restaurante indicando su capacidad y tipo de ocasión**,
> para que **el módulo de reservas tenga siempre información actualizada para la asignación automática**.

**Criterios de Aceptación:**
1. `POST /api/mesas` crea una mesa con `numero`, `capacidad` y `tipo_ocasion`; retorna HTTP 201.
2. `PUT /api/mesas/:id` edita datos de la mesa; retorna HTTP 200.
3. `PATCH /api/mesas/:id/estado` desactiva la mesa; retorna HTTP 200.
4. Mesa con número duplicado retorna HTTP 409.
5. `tipo_ocasion` inválido (distinto de familiar, romantica, reunion) retorna HTTP 400.
6. La UI muestra las mesas en tabla con badge de tipo y estado, formulario modal de creación/edición.

**Desglose de Tareas Técnicas:**

| ID | Capa | Tarea | Prompt SDD para IA |
|----|------|-------|--------------------|
| T1 | Backend | Crear funciones CRUD de mesas en `mesa_service.py` | RF-08 |
| T2 | Backend | Crear `mesas_routes.py` con endpoints #10..#13 y `@rol_requerido("ADMIN")` | `architecture.md` endpoints #10..#13 |
| T3 | Tests | Escribir `test_mesa_service.py`: CRUD, número duplicado, tipo_ocasion inválido, desactivar | Cobertura |
| T4 | Frontend | Crear `MesasPage.jsx` con tabla de mesas, modal de formulario y toggle de estado | RF-08 |

---

#### HU-17 — Gestionar configuración del sistema

| Campo | Detalle |
|-------|---------|
| **ID** | HU-17 |
| **Épica** | EP-05 — Panel de Administración |
| **Prioridad** | Baja |
| **Estimación** | 3 puntos / aprox. 5 horas ideales |
| **Sprint** | Sprint 4 |
| **RF asociado** | RF-22 |

**Historia:**
> Como **administrador**,
> quiero **modificar los parámetros generales del sistema desde el panel (nombre del negocio, horario de atención, número de contacto)**,
> para que **la información del restaurante siempre esté actualizada sin necesidad de modificar el código**.

**Criterios de Aceptación:**
1. `GET /api/admin/configuracion` retorna todos los pares clave-valor de la tabla `Configuracion`; HTTP 200.
2. `PUT /api/admin/configuracion` actualiza uno o varios parámetros; retorna HTTP 200.
3. Clave de configuración no reconocida retorna HTTP 400.
4. Los cambios en `jwt_expiration_hours` se aplican a tokens nuevos emitidos después del cambio.
5. La UI muestra un formulario con los campos de configuración pre-llenados y botón "Guardar cambios".

**Desglose de Tareas Técnicas:**

| ID | Capa | Tarea | Prompt SDD para IA |
|----|------|-------|--------------------|
| T1 | BD | Verificar seed data de tabla `Configuracion` con claves: nombre_negocio, horario_apertura, horario_cierre, contacto, jwt_expiration_hours | `database.md` |
| T2 | Backend | Crear endpoints `GET` y `PUT /api/admin/configuracion` con `@rol_requerido("ADMIN")` | `architecture.md` endpoints #34, #35 |
| T3 | Frontend | Crear `ConfiguracionPage.jsx` con formulario pre-llenado desde la API | RF-22 |

---

## 6. PRODUCT BACKLOG — RESUMEN VISUAL

```
SPRINT 1 — Fundamentos y Seguridad (15 pts)
├── HU-01  Configuración base y BD                    [5 pts] ████████
├── HU-02  Login JWT                                  [3 pts] █████
├── HU-03  Gestión de usuarios (CRUD Admin)           [5 pts] ████████
└── HU-04  Cambiar contraseña                         [2 pts] ███

SPRINT 2 — Motor de Reservas (19 pts)
├── HU-05  Registrar reserva + asignación automática  [8 pts] █████████████
├── HU-06  Consultar disponibilidad                   [3 pts] █████
├── HU-07  Listar y actualizar reservas               [5 pts] ████████
└── HU-08  Cancelar reserva con código                [3 pts] █████

SPRINT 3 — Carta Digital (11 pts)
├── HU-09  Visualizar carta pública                   [3 pts] █████
├── HU-10  Gestionar categorías                       [3 pts] █████
└── HU-11  Gestionar platillos                        [5 pts] ████████

SPRINT 4 — Takeaway y Panel Admin (26 pts)
├── HU-12  Realizar pedido takeaway                   [8 pts] █████████████
├── HU-13  Consultar estado pedido (cliente)          [2 pts] ███
├── HU-14  Listar y actualizar pedidos                [5 pts] ████████
├── HU-15  Dashboard de administración                [5 pts] ████████
├── HU-16  Gestionar mesas                            [3 pts] █████
└── HU-17  Configuración del sistema                  [3 pts] █████

TOTAL: 17 historias — 71 puntos de historia
```

---

## 7. MATRIZ DE TRAZABILIDAD HU → RF → FUNCIÓN CRÍTICA

| Historia | RF asociado | Función crítica (pytest ≥ 90%) | Sprint |
|----------|-------------|-------------------------------|--------|
| HU-02 | RF-25, RF-26 | `autenticar_usuario()` (#3) | S1 |
| HU-04 | RF-28 | `autenticar_usuario()` (#3) | S1 |
| HU-05 | RF-01, RF-02, RF-04 | `asignar_mesa_automatica()` (#1), `crear_reserva()` (#2), `validar_disponibilidad_mesa()` (#7) | S2 |
| HU-06 | RF-03 | `validar_disponibilidad_mesa()` (#7) | S2 |
| HU-07 | RF-05, RF-06 | — | S2 |
| HU-08 | RF-07 | — | S2 |
| HU-09 | RF-09, RF-10 | `cambiar_visibilidad_platillo()` (#8) | S3 |
| HU-11 | RF-12, RF-13 | `cambiar_visibilidad_platillo()` (#8) | S3 |
| HU-12 | RF-14, RF-15, RF-16 | `calcular_total_pedido()` (#4), `crear_pedido_takeaway()` (#5) | S4 |
| HU-14 | RF-17, RF-18, RF-20 | `actualizar_estado_pedido()` (#6) | S4 |

---

## 8. DEFINICIÓN DE TERMINADO (Definition of Done)

Una historia de usuario se considera **COMPLETADA** cuando cumple todos los criterios siguientes:

| # | Criterio | Verificación |
|---|----------|--------------|
| 1 | Todos los criterios de aceptación pasan | Revisión manual en entorno local |
| 2 | Los endpoints asociados responden con los códigos HTTP correctos | Prueba en Postman / pytest integration |
| 3 | Las pruebas unitarias de las funciones de servicio involucradas pasan | `pytest tests/unit/ -v` sin fallos |
| 4 | La cobertura acumulada de `app/services/` se mantiene ≥ 90% | `pytest --cov=app/services --cov-fail-under=90` |
| 5 | El código generado por IA fue revisado y ajustado por el desarrollador | Commit en rama feature con PR aprobado |
| 6 | El componente React correspondiente renderiza sin errores de consola | Inspección en Chrome DevTools |
| 7 | La interfaz es responsiva en viewport móvil (375px) y escritorio (1440px) | Prueba en Chrome DevTools responsive mode |
| 8 | El código está en GitHub en la rama `main` o fusionado por PR | `git log --oneline` en rama main |

---

## 9. HISTORIAL DE VERSIONES

| Versión | Fecha | Descripción |
|---------|-------|-------------|
| 1.0.0 | Junio 2026 | Versión inicial — 17 historias de usuario distribuidas en 4 Sprints |

---

*Documento generado como parte de la metodología Spec Driven Development (SDD) para el proyecto académico IS-489 — UNSCH 2026. Cada historia de usuario incluye el prompt SDD que guía a la IA en la generación del código correspondiente durante la fase de implementación.*
