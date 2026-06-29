# requirements.md
# Sistema Integral de Gestión para Pollería Leña y Carbón
**Especificación de Requerimientos — Spec Driven Development (SDD)**
**Curso:** IS-489 Pruebas y Aseguramiento de Calidad — UNSCH 2026
**Versión:** 1.0.0 | **Fecha:** Junio 2026

---

## 1. DESCRIPCIÓN GENERAL DEL SISTEMA

### 1.1. Propósito
El presente documento especifica los requerimientos funcionales y no funcionales del **Sistema Integral de Gestión para Pollería Leña y Carbón**, una plataforma web desarrollada bajo la metodología Spec Driven Development (SDD) con el marco de trabajo ágil Scrum. Este documento sirve como contrato técnico que guiará la generación de código asistida por Inteligencia Artificial, así como la definición de las pruebas unitarias y de integración con cobertura mínima del 90%.

### 1.2. Alcance del Sistema
El sistema gestiona cinco módulos principales para una pollería de tipo restaurante:

| N.° | Módulo | Descripción resumida |
|-----|--------|----------------------|
| M-01 | Reservas | Registro y asignación automática de mesas según tipo de ocasión |
| M-02 | Carta Digital | Visualización del menú por categorías y platillos disponibles |
| M-03 | Takeaway | Pedidos para llevar con seguimiento de estado |
| M-04 | Panel de Administración | Gestión centralizada del negocio por el administrador |
| M-05 | Usuarios y Roles | Autenticación, autorización y gestión de cuentas |

### 1.3. Actores del Sistema
| Actor | Tipo | Descripción |
|-------|------|-------------|
| Cliente | Externo | Accede al sistema sin registro obligatorio para consultar la carta y realizar reservas o pedidos takeaway |
| Recepcionista | Interno | Gestiona reservas, atiende pedidos takeaway y administra la operación diaria |
| Administrador | Interno | Tiene acceso total: gestiona carta, usuarios, mesas, configuración y reportes |

### 1.4. Exclusiones explícitas del alcance
Los siguientes elementos están **fuera del alcance** del sistema y no deben implementarse:
- Delivery / reparto a domicilio
- Mapa visual interactivo de mesas
- Panel de Cocina (KDS — Kitchen Display System)
- Pedidos realizados por mozo desde una tablet
- Lectura de QR en mesa para ordenar
- Arquitectura multi-tenant / SaaS

---

## 2. REQUERIMIENTOS FUNCIONALES

### 2.1. Módulo M-01: Reservas

| Código | Nombre | Descripción | Actor |
|--------|--------|-------------|-------|
| RF-01 | Registrar reserva | El sistema permitirá que un cliente registre una reserva indicando nombre, fecha, hora, número de personas y tipo de ocasión (familiar, romántica, reunión). | Cliente |
| RF-02 | Asignación automática de mesa | Al crear una reserva, el sistema asignará automáticamente una mesa disponible según el tipo de ocasión y capacidad requerida, sin intervención manual del recepcionista. | Sistema |
| RF-03 | Consultar disponibilidad | El sistema mostrará los horarios y fechas disponibles antes de confirmar la reserva. | Cliente |
| RF-04 | Confirmar reserva | El sistema generará un código de confirmación único para cada reserva registrada exitosamente. | Sistema |
| RF-05 | Listar reservas del día | El recepcionista podrá visualizar todas las reservas del día actual con su estado (pendiente, confirmada, cancelada, completada). | Recepcionista |
| RF-06 | Actualizar estado de reserva | El recepcionista podrá cambiar el estado de una reserva (confirmar, completar, cancelar). | Recepcionista |
| RF-07 | Cancelar reserva | El cliente podrá cancelar su reserva mediante el código de confirmación, siempre que sea con al menos 1 hora de anticipación. | Cliente |
| RF-08 | Gestionar mesas | El administrador podrá registrar, editar y desactivar mesas, especificando capacidad y tipo de ocasión para la que están habilitadas. | Administrador |

### 2.2. Módulo M-02: Carta Digital

| Código | Nombre | Descripción | Actor |
|--------|--------|-------------|-------|
| RF-09 | Visualizar carta | El sistema mostrará la carta digital organizada por categorías con el nombre, descripción, precio e imagen de cada platillo. | Cliente |
| RF-10 | Filtrar por categoría | El cliente podrá filtrar los platillos por categoría (pollos, bebidas, guarniciones, postres, etc.). | Cliente |
| RF-11 | Gestionar categorías | El administrador podrá crear, editar y eliminar categorías de la carta. | Administrador |
| RF-12 | Gestionar platillos | El administrador podrá crear, editar, activar y desactivar platillos de la carta, incluyendo nombre, descripción, precio, imagen y categoría. | Administrador |
| RF-13 | Activar/desactivar platillo | El administrador podrá cambiar la visibilidad de un platillo en la carta sin eliminarlo del sistema. | Administrador |

### 2.3. Módulo M-03: Takeaway

| Código | Nombre | Descripción | Actor |
|--------|--------|-------------|-------|
| RF-14 | Realizar pedido takeaway | El cliente podrá seleccionar platillos de la carta digital y registrar un pedido para llevar, indicando nombre, número de contacto y hora estimada de recojo. | Cliente |
| RF-15 | Agregar ítems al pedido | El sistema permitirá agregar múltiples platillos con sus respectivas cantidades al pedido takeaway antes de confirmarlo. | Cliente |
| RF-16 | Confirmar pedido takeaway | Al confirmar el pedido, el sistema generará un código de seguimiento y calculará el total a pagar. | Sistema |
| RF-17 | Listar pedidos takeaway | El recepcionista visualizará todos los pedidos takeaway con su estado (recibido, en preparación, listo, entregado, cancelado). | Recepcionista |
| RF-18 | Actualizar estado del pedido | El recepcionista podrá actualizar el estado del pedido takeaway conforme avanza su preparación. | Recepcionista |
| RF-19 | Consultar estado del pedido | El cliente podrá consultar el estado actual de su pedido ingresando el código de seguimiento. | Cliente |
| RF-20 | Cancelar pedido takeaway | El recepcionista podrá cancelar un pedido takeaway únicamente si su estado es "recibido". | Recepcionista |

### 2.4. Módulo M-04: Panel de Administración

| Código | Nombre | Descripción | Actor |
|--------|--------|-------------|-------|
| RF-21 | Ver dashboard | El administrador tendrá acceso a un panel con métricas del día: total de reservas, pedidos takeaway, ingresos estimados y platillos más solicitados. | Administrador |
| RF-22 | Gestionar configuración | El administrador podrá modificar los parámetros generales del sistema: nombre del negocio, horario de atención, número de contacto y capacidad máxima. | Administrador |
| RF-23 | Ver historial de reservas | El administrador podrá consultar el historial completo de reservas filtrando por fecha y estado. | Administrador |
| RF-24 | Ver historial de pedidos | El administrador podrá consultar el historial de pedidos takeaway filtrando por fecha y estado. | Administrador |

### 2.5. Módulo M-05: Usuarios y Roles

| Código | Nombre | Descripción | Actor |
|--------|--------|-------------|-------|
| RF-25 | Iniciar sesión | Los usuarios con rol Recepcionista y Administrador podrán autenticarse con correo y contraseña. El sistema generará un token JWT con vigencia de 8 horas. | Recepcionista / Administrador |
| RF-26 | Cerrar sesión | El sistema invalidará el token JWT activo al cerrar sesión. | Recepcionista / Administrador |
| RF-27 | Gestionar usuarios | El administrador podrá crear, editar, activar y desactivar cuentas de usuarios del sistema (solo roles Recepcionista y Administrador). | Administrador |
| RF-28 | Cambiar contraseña | El usuario autenticado podrá cambiar su contraseña ingresando la contraseña actual y la nueva. | Recepcionista / Administrador |
| RF-29 | Control de acceso por rol | El sistema restringirá el acceso a rutas y funcionalidades según el rol del usuario autenticado. Las rutas protegidas devolverán HTTP 401 o 403 según corresponda. | Sistema |

---

## 3. REQUERIMIENTOS NO FUNCIONALES

| Código | Categoría | Requerimiento | Métrica / Criterio de aceptación |
|--------|-----------|---------------|----------------------------------|
| RNF-01 | Rendimiento | El sistema debe responder a las solicitudes de la API REST en menos de 800 ms bajo condiciones normales de uso. | Tiempo de respuesta ≤ 800 ms en endpoints críticos medido con Postman. |
| RNF-02 | Seguridad | Todas las contraseñas deben almacenarse en la base de datos utilizando hashing con `bcrypt` (mínimo 12 rounds). | Ninguna contraseña en texto plano en la base de datos. |
| RNF-03 | Seguridad | El acceso a rutas protegidas debe validarse mediante tokens JWT firmados. Los tokens expirados o inválidos deben retornar HTTP 401. | 100% de rutas protegidas requieren token válido. |
| RNF-04 | Disponibilidad | El sistema debe estar disponible al menos el 95% del tiempo durante el horario de atención del restaurante (8:00 a.m. – 11:00 p.m.). | Uptime ≥ 95% verificado en el entorno de despliegue (Render/Railway). |
| RNF-05 | Mantenibilidad | El código del backend debe seguir la arquitectura en tres capas (Routes → Services → Models) para facilitar las pruebas unitarias. | Cada capa tiene responsabilidad única; la capa de servicios es independientemente testeable con pytest. |
| RNF-06 | Cobertura de pruebas | Las pruebas unitarias implementadas con pytest deben alcanzar una cobertura mínima del 90% sobre las funciones de la capa de servicios (lógica de negocio). | `pytest --cov` reporta ≥ 90% de cobertura en `/backend/services/`. |
| RNF-07 | Usabilidad | La interfaz de usuario debe ser responsiva y accesible desde dispositivos móviles y de escritorio. | El frontend se adapta correctamente a viewports desde 375 px (móvil) hasta 1440 px (escritorio). |
| RNF-08 | Portabilidad | El sistema debe poder desplegarse en entornos de nube como Render o Railway sin modificaciones al código fuente. | Despliegue exitoso documentado con URL pública funcional. |
| RNF-09 | Escalabilidad | La arquitectura desacoplada (API REST + SPA) debe permitir que el frontend y el backend escalen de forma independiente. | Frontend e implementación de backend son proyectos separados con sus propios procesos de despliegue. |
| RNF-10 | Integridad de datos | La base de datos MySQL debe implementar restricciones de integridad referencial (FOREIGN KEY con ON DELETE RESTRICT o CASCADE según corresponda) para evitar registros huérfanos. | El script DDL incluye todas las restricciones de integridad referencial definidas en el diagrama ER. |

---

## 4. RESTRICCIONES TÉCNICAS

| Restricción | Detalle |
|-------------|---------|
| Lenguaje backend | Python 3.11+ con Flask 3.x |
| ORM | Flask-SQLAlchemy 3.x con MySQL 8.x |
| Serialización | Marshmallow 3.x para validación y serialización de datos |
| Autenticación | Flask-JWT-Extended (tokens JWT, expiración configurable) |
| Frontend | React 18+ con Vite, Tailwind CSS 3.x, shadcn/ui |
| Gestión de estado | Zustand 4.x |
| Formularios | React Hook Form + Zod (validación en cliente) |
| HTTP client | Axios 1.x |
| Pruebas | pytest 8.x + pytest-cov (cobertura ≥ 90%) |
| Control de versiones | Git + GitHub (repositorio público o privado) |
| Base de datos | MySQL 8.x (InnoDB, UTF-8 mb4) |
| Despliegue | Backend en Render o Railway; Frontend en Vercel o Render Static |

---

## 5. REGLAS DE NEGOCIO

| Código | Regla |
|--------|-------|
| RN-01 | Una mesa solo puede tener una reserva activa (estado: pendiente o confirmada) en el mismo tramo horario. El tramo horario de bloqueo es de 2 horas a partir de la hora de reserva. |
| RN-02 | La asignación automática de mesa prioriza: (a) disponibilidad de horario, (b) tipo de ocasión compatible, (c) capacidad mínima suficiente para el número de personas. |
| RN-03 | Los tipos de ocasión y sus criterios de asignación son: **familiar** → mesas de ≥ 4 personas; **romántica** → mesas de 2 personas con ambiente privado; **reunión** → mesas de ≥ 6 personas. |
| RN-04 | Si no existe mesa disponible que cumpla los criterios, el sistema debe retornar un mensaje de error claro y no crear la reserva. |
| RN-05 | Un pedido takeaway solo puede cancelarse si su estado es "recibido". Una vez en estado "en preparación", no puede cancelarse. |
| RN-06 | El precio de un pedido takeaway se calcula como la suma de (precio unitario × cantidad) de cada ítem. El precio se fija en el momento de la confirmación y no varía si cambia el precio del platillo en la carta. |
| RN-07 | Solo el Administrador puede crear, editar o desactivar usuarios del sistema. El rol "Cliente" no tiene cuenta en el sistema. |
| RN-08 | Un platillo desactivado no aparece en la carta digital pública, pero sus registros históricos en pedidos se conservan. |
| RN-09 | Una categoría no puede eliminarse si tiene platillos activos asociados. Primero deben desactivarse o reasignarse los platillos. |
| RN-10 | El token JWT incluirá en su payload: `user_id`, `email`, `rol` y `exp`. El tiempo de expiración se leerá de la tabla `Configuracion`. |

---

## 6. CASOS DE USO PRINCIPALES

### CU-01: Realizar Reserva
- **Actor principal:** Cliente
- **Precondición:** El sistema tiene mesas activas registradas.
- **Flujo principal:**
  1. El cliente accede al módulo de Reservas.
  2. Ingresa nombre, fecha, hora, número de personas y tipo de ocasión.
  3. El sistema verifica disponibilidad de mesas compatibles.
  4. El sistema asigna automáticamente la mesa más adecuada (RN-01, RN-02, RN-03).
  5. El sistema registra la reserva con estado "pendiente" y genera un código de confirmación.
  6. El sistema muestra el código de confirmación al cliente.
- **Flujo alterno A — Sin mesa disponible:**
  - 3a. No existe mesa compatible disponible → el sistema retorna HTTP 409 con mensaje "No hay mesas disponibles para el horario y tipo de ocasión seleccionados."
- **Flujo alterno B — Datos inválidos:**
  - 2b. El cliente omite campos obligatorios → el sistema retorna HTTP 400 con detalle de campos inválidos.

### CU-02: Iniciar Sesión
- **Actor principal:** Recepcionista / Administrador
- **Flujo principal:**
  1. El usuario ingresa correo y contraseña.
  2. El sistema valida las credenciales contra la base de datos.
  3. El sistema verifica que la cuenta esté activa.
  4. El sistema genera y retorna un token JWT con los datos del usuario.
- **Flujo alterno A — Credenciales incorrectas:**
  - 2a. Las credenciales no coinciden → HTTP 401 con mensaje "Credenciales inválidas."
- **Flujo alterno B — Cuenta inactiva:**
  - 3b. La cuenta está desactivada → HTTP 403 con mensaje "Cuenta desactivada. Contacte al administrador."

### CU-03: Realizar Pedido Takeaway
- **Actor principal:** Cliente
- **Precondición:** La carta digital tiene platillos activos.
- **Flujo principal:**
  1. El cliente selecciona platillos de la carta y especifica cantidades.
  2. El cliente ingresa nombre y número de contacto.
  3. El cliente confirma el pedido.
  4. El sistema calcula el total (RN-06) y genera un código de seguimiento.
  5. El sistema registra el pedido con estado "recibido".
  6. El sistema retorna el código de seguimiento y el total al cliente.
- **Flujo alterno A — Carrito vacío:**
  - 3a. El cliente intenta confirmar sin ítems → HTTP 400 "El pedido debe contener al menos un platillo."
- **Flujo alterno B — Platillo no disponible:**
  - 1b. Un platillo fue desactivado mientras el cliente lo tenía en el carrito → HTTP 422 indicando el platillo no disponible.

### CU-04: Gestionar Carta Digital
- **Actor principal:** Administrador
- **Flujo principal:**
  1. El administrador accede al Panel de Administración → sección Carta.
  2. Puede crear una categoría nueva o seleccionar una existente.
  3. Crea un platillo asignándolo a una categoría, con nombre, descripción, precio e imagen.
  4. El platillo queda activo y visible en la carta pública.
- **Flujo alterno — Eliminar categoría con platillos activos:**
  - El sistema retorna HTTP 409 "No se puede eliminar una categoría con platillos activos." (RN-09)

### CU-05: Gestionar Usuarios
- **Actor principal:** Administrador
- **Flujo principal:**
  1. El administrador accede a la sección Usuarios del Panel.
  2. Crea un usuario nuevo con nombre, correo, contraseña temporal y rol (Recepcionista o Administrador).
  3. El sistema hashea la contraseña con bcrypt y guarda el registro activo.
  4. El nuevo usuario puede iniciar sesión con sus credenciales.
- **Flujo alterno — Correo duplicado:**
  - El sistema retorna HTTP 409 "El correo electrónico ya está registrado."

---

## 7. FUNCIONES CRÍTICAS PARA COBERTURA DE PRUEBAS (≥ 90%)

Las siguientes funciones de la capa de servicios son consideradas críticas para el negocio y deben tener cobertura de pruebas unitarias completa:

| N.° | Función / Servicio | Módulo | Tipo de prueba prioritaria |
|-----|--------------------|--------|-----------------------------|
| 1 | `asignar_mesa_automatica(fecha, hora, personas, tipo_ocasion)` | Reservas | Unitaria — caja blanca (todos los flujos de RN-01 a RN-04) |
| 2 | `crear_reserva(datos)` | Reservas | Unitaria + integración con BD |
| 3 | `autenticar_usuario(email, password)` | Usuarios | Unitaria — flujos válidos e inválidos |
| 4 | `calcular_total_pedido(items)` | Takeaway | Unitaria — caja blanca |
| 5 | `crear_pedido_takeaway(datos)` | Takeaway | Unitaria + integración con BD |
| 6 | `actualizar_estado_pedido(pedido_id, nuevo_estado)` | Takeaway | Unitaria — validación de transiciones de estado |
| 7 | `validar_disponibilidad_mesa(mesa_id, fecha, hora)` | Reservas | Unitaria — caja blanca con conflictos de horario |
| 8 | `cambiar_visibilidad_platillo(platillo_id, activo)` | Carta Digital | Unitaria |

---

## 8. ENTIDADES Y ATRIBUTOS PRINCIPALES

| Entidad | Atributos clave |
|---------|-----------------|
| **Usuario** | id, nombre, email, password_hash, rol (ADMIN, RECEPCIONISTA), activo, created_at |
| **Mesa** | id, numero, capacidad, tipo_ocasion (familiar, romantica, reunion), activo |
| **Reserva** | id, cliente_nombre, cliente_contacto, fecha, hora, num_personas, tipo_ocasion, estado, codigo_confirmacion, mesa_id (FK), created_at |
| **Categoria** | id, nombre, descripcion, activo |
| **Platillo** | id, nombre, descripcion, precio, imagen_url, activo, categoria_id (FK) |
| **PedidoTakeaway** | id, cliente_nombre, cliente_contacto, total, estado, codigo_seguimiento, created_at |
| **DetallePedido** | id, pedido_id (FK), platillo_id (FK), cantidad, precio_unitario |
| **Configuracion** | id, clave, valor (ej: jwt_expiration_hours, horario_apertura, horario_cierre, nombre_negocio) |

---

## 9. ESTRUCTURA DE CARPETAS DEL PROYECTO

```
polleria-lena-carbon/
├── .kiro/
│   └── specs/
│       ├── requirements.md        ← este archivo
│       ├── architecture.md
│       ├── user-stories.md
│       └── database.md
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── routes/               ← endpoints REST (Capa 1)
│   │   ├── services/             ← lógica de negocio (Capa 2) ← COBERTURA 90%
│   │   ├── models/               ← SQLAlchemy models (Capa 3)
│   │   └── schemas/              ← Marshmallow schemas
│   ├── config.py
│   ├── requirements.txt
│   └── run.py
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── services/             ← llamadas Axios a la API
│   │   ├── store/                ← Zustand stores
│   │   └── schemas/              ← Zod schemas
│   ├── package.json
│   └── vite.config.js
└── tests/
    ├── unit/                     ← pytest pruebas unitarias por servicio
    ├── integration/              ← pruebas de integración con BD de prueba
    └── conftest.py
```

---

## 10. CRITERIOS DE ACEPTACIÓN GLOBALES

| Criterio | Condición de éxito |
|----------|--------------------|
| Cobertura de pruebas | `pytest --cov=app/services --cov-report=term-missing` reporta ≥ 90% |
| CI en GitHub | El repositorio tiene un workflow de GitHub Actions que ejecuta pytest en cada push |
| Despliegue | El sistema está disponible en una URL pública funcional (Render/Railway + Vercel) |
| API documentada | Los 25+ endpoints están documentados en el archivo `architecture.md` con método, ruta, body y respuestas |
| Sin datos en texto plano | Ninguna contraseña ni token aparece en texto plano en la base de datos o en los logs |
| Roles funcionando | Un usuario con rol RECEPCIONISTA no puede acceder a rutas exclusivas del ADMINISTRADOR (retorna HTTP 403) |

---

## 11. HISTORIAL DE VERSIONES

| Versión | Fecha | Descripción |
|---------|-------|-------------|
| 1.0.0 | Junio 2026 | Versión inicial — especificación completa de requerimientos SDD |

---

*Documento generado como parte de la metodología Spec Driven Development (SDD) para el proyecto académico IS-489 — UNSCH 2026. Este archivo es el contrato base que guía la generación de código mediante Inteligencia Artificial en las fases siguientes del proyecto.*
