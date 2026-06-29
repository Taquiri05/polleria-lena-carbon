# database.md
# Sistema Integral de Gestión para Pollería Leña y Carbón
**Especificación de Base de Datos — Spec Driven Development (SDD)**
**Curso:** IS-489 Pruebas y Aseguramiento de Calidad — UNSCH 2026
**Versión:** 1.0.0 | **Fecha:** Junio 2026

---

## 1. DECISIONES DE DISEÑO DE BASE DE DATOS

| Decisión | Valor | Justificación |
|----------|-------|---------------|
| Motor | MySQL 8.x | Soporte ACID completo via InnoDB; amplia compatibilidad con Flask-SQLAlchemy y PyMySQL |
| Storage Engine | InnoDB | Garantiza integridad referencial (FK), transacciones y bloqueo a nivel de fila |
| Charset | `utf8mb4` | Soporte completo de Unicode (tildes, ñ, emojis en descripciones de platillos) |
| Collation | `utf8mb4_unicode_ci` | Comparaciones de texto insensibles a mayúsculas y tildes |
| Zona horaria | `America/Lima` (UTC-5) | Registros temporales alineados al horario operativo del restaurante |
| Naming convention | `snake_case` en singular | Consistencia con modelos SQLAlchemy y convención Python |
| Claves primarias | `INT AUTO_INCREMENT` | Sencillez y rendimiento en JOINs; sin UUID para reducir complejidad |
| Borrado | Lógico (`activo BOOLEAN`) | Preserva historial de pedidos y reservas; nunca DELETE físico en entidades de negocio |

---

## 2. DIAGRAMA ENTIDAD-RELACIÓN (DER)

```
┌──────────────────────────────────────────────────────────────────────────────┐
│                    DIAGRAMA ENTIDAD-RELACIÓN                                 │
│            Sistema Integral de Gestión — Pollería Leña y Carbón              │
└──────────────────────────────────────────────────────────────────────────────┘

 ┌─────────────────────┐          ┌──────────────────────────────────┐
 │      usuario        │          │             reserva               │
 ├─────────────────────┤          ├──────────────────────────────────┤
 │ PK id               │          │ PK id                            │
 │    nombre           │          │    cliente_nombre                │
 │    email      UQ    │          │    cliente_contacto              │
 │    password_hash    │          │    fecha                         │
 │    rol       ENUM   │          │    hora                          │
 │    activo    BOOL   │          │    num_personas                  │
 │    created_at       │          │    tipo_ocasion  ENUM            │
 └─────────────────────┘          │    estado        ENUM            │
                                  │    codigo_confirmacion     UQ    │
                                  │ FK mesa_id ──────────────────┐   │
                                  │    created_at                │   │
                                  └──────────────────────────────┼───┘
                                                                 │
 ┌─────────────────────┐          ┌────────────────────────────  │ ──┐
 │        mesa         │◀─────────│                              │   │
 ├─────────────────────┤  1    N  │  (FK mesa_id referencia      │   │
 │ PK id               │          │   a mesa.id)                 │   │
 │    numero     UQ    │          └──────────────────────────────┘   │
 │    capacidad        │
 │    tipo_ocasion     │
 │         ENUM        │
 │    activo    BOOL   │
 └─────────────────────┘

 ┌─────────────────────┐          ┌─────────────────────┐
 │      categoria      │          │      platillo        │
 ├─────────────────────┤  1    N  ├─────────────────────┤
 │ PK id               │◀─────────│ PK id               │
 │    nombre     UQ    │          │    nombre            │
 │    descripcion      │          │    descripcion       │
 │    activo    BOOL   │          │    precio    DEC     │
 └─────────────────────┘          │    imagen_url        │
                                  │    activo    BOOL    │
                                  │ FK categoria_id      │
                                  └──────────┬───────────┘
                                             │
                                             │ 1
                                             │
                                  ┌──────────▼───────────┐
                                  │    detalle_pedido     │
                                  ├──────────────────────┤
                                  │ PK id                │
                                  │ FK pedido_id ──────┐ │
                                  │ FK platillo_id      │ │
                                  │    cantidad          │ │
                                  │    precio_unitario   │ │
                                  └──────────────────────┼─┘
                                                         │ N
                                                         │
 ┌─────────────────────┐          ┌──────────────────────▼───────┐
 │    configuracion    │          │       pedido_takeaway         │
 ├─────────────────────┤          ├──────────────────────────────┤
 │ PK id               │          │ PK id                        │
 │    clave      UQ    │          │    cliente_nombre             │
 │    valor            │          │    cliente_contacto           │
 └─────────────────────┘          │    total          DEC        │
                                  │    estado         ENUM       │
                                  │    codigo_seguimiento  UQ    │
                                  │    created_at                │
                                  └──────────────────────────────┘
```

### 2.1. Relaciones entre entidades

| Relación | Cardinalidad | FK | ON DELETE |
|----------|-------------|-----|-----------|
| `categoria` → `platillo` | 1 : N | `platillo.categoria_id` → `categoria.id` | `RESTRICT` |
| `mesa` → `reserva` | 1 : N | `reserva.mesa_id` → `mesa.id` | `RESTRICT` |
| `pedido_takeaway` → `detalle_pedido` | 1 : N | `detalle_pedido.pedido_id` → `pedido_takeaway.id` | `CASCADE` |
| `platillo` → `detalle_pedido` | 1 : N | `detalle_pedido.platillo_id` → `platillo.id` | `RESTRICT` |

**Justificación de `ON DELETE`:**
- `RESTRICT` en `categoria → platillo`: no se puede eliminar una categoría si tiene platillos (RN-09).
- `RESTRICT` en `mesa → reserva`: no se puede eliminar una mesa con reservas históricas.
- `CASCADE` en `pedido_takeaway → detalle_pedido`: al eliminar un pedido (operación admin interna), sus ítems se eliminan con él.
- `RESTRICT` en `platillo → detalle_pedido`: un platillo no se puede eliminar si aparece en pedidos históricos (RN-08).

---

## 3. SCRIPT DDL COMPLETO — MySQL 8.x

```sql
-- ============================================================
-- DDL: Sistema Integral de Gestión — Pollería Leña y Carbón
-- Motor: MySQL 8.x | InnoDB | utf8mb4_unicode_ci
-- Generado para: IS-489 UNSCH 2026 — SDD
-- ============================================================

-- Crear y seleccionar la base de datos
CREATE DATABASE IF NOT EXISTS polleria_lena_carbon
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE polleria_lena_carbon;

-- Configurar zona horaria de sesión
SET time_zone = '-05:00';

-- ============================================================
-- TABLA 1: usuario
-- ============================================================
CREATE TABLE IF NOT EXISTS usuario (
    id            INT           NOT NULL AUTO_INCREMENT,
    nombre        VARCHAR(100)  NOT NULL,
    email         VARCHAR(150)  NOT NULL,
    password_hash VARCHAR(255)  NOT NULL,
    rol           ENUM('ADMIN', 'RECEPCIONISTA') NOT NULL DEFAULT 'RECEPCIONISTA',
    activo        BOOLEAN       NOT NULL DEFAULT TRUE,
    created_at    DATETIME      NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT pk_usuario PRIMARY KEY (id),
    CONSTRAINT uq_usuario_email UNIQUE (email),
    INDEX idx_usuario_rol (rol),
    INDEX idx_usuario_activo (activo)
) ENGINE=InnoDB
  DEFAULT CHARSET=utf8mb4
  COLLATE=utf8mb4_unicode_ci
  COMMENT='Usuarios del sistema con acceso al panel (staff del restaurante)';


-- ============================================================
-- TABLA 2: mesa
-- ============================================================
CREATE TABLE IF NOT EXISTS mesa (
    id            INT           NOT NULL AUTO_INCREMENT,
    numero        INT           NOT NULL,
    capacidad     TINYINT       NOT NULL,
    tipo_ocasion  ENUM('familiar', 'romantica', 'reunion') NOT NULL,
    activo        BOOLEAN       NOT NULL DEFAULT TRUE,

    CONSTRAINT pk_mesa PRIMARY KEY (id),
    CONSTRAINT uq_mesa_numero UNIQUE (numero),
    CONSTRAINT chk_mesa_capacidad CHECK (capacidad >= 1 AND capacidad <= 30),
    INDEX idx_mesa_tipo_ocasion (tipo_ocasion),
    INDEX idx_mesa_activo (activo),
    INDEX idx_mesa_disponibilidad (activo, tipo_ocasion, capacidad)
) ENGINE=InnoDB
  DEFAULT CHARSET=utf8mb4
  COLLATE=utf8mb4_unicode_ci
  COMMENT='Mesas físicas del restaurante disponibles para reservas';


-- ============================================================
-- TABLA 3: reserva
-- ============================================================
CREATE TABLE IF NOT EXISTS reserva (
    id                   INT          NOT NULL AUTO_INCREMENT,
    cliente_nombre       VARCHAR(100) NOT NULL,
    cliente_contacto     VARCHAR(20)  NOT NULL,
    fecha                DATE         NOT NULL,
    hora                 TIME         NOT NULL,
    num_personas         TINYINT      NOT NULL,
    tipo_ocasion         ENUM('familiar', 'romantica', 'reunion') NOT NULL,
    estado               ENUM('pendiente', 'confirmada', 'completada', 'cancelada')
                                      NOT NULL DEFAULT 'pendiente',
    codigo_confirmacion  VARCHAR(20)  NOT NULL,
    mesa_id              INT          NOT NULL,
    created_at           DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT pk_reserva PRIMARY KEY (id),
    CONSTRAINT uq_reserva_codigo UNIQUE (codigo_confirmacion),
    CONSTRAINT chk_reserva_personas CHECK (num_personas >= 1 AND num_personas <= 30),
    CONSTRAINT fk_reserva_mesa
        FOREIGN KEY (mesa_id) REFERENCES mesa (id)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,
    INDEX idx_reserva_fecha (fecha),
    INDEX idx_reserva_estado (estado),
    INDEX idx_reserva_mesa_fecha (mesa_id, fecha, hora),
    INDEX idx_reserva_codigo (codigo_confirmacion),
    INDEX idx_reserva_fecha_estado (fecha, estado)
) ENGINE=InnoDB
  DEFAULT CHARSET=utf8mb4
  COLLATE=utf8mb4_unicode_ci
  COMMENT='Reservas de mesas realizadas por clientes del restaurante';


-- ============================================================
-- TABLA 4: categoria
-- ============================================================
CREATE TABLE IF NOT EXISTS categoria (
    id           INT          NOT NULL AUTO_INCREMENT,
    nombre       VARCHAR(100) NOT NULL,
    descripcion  TEXT,
    activo       BOOLEAN      NOT NULL DEFAULT TRUE,

    CONSTRAINT pk_categoria PRIMARY KEY (id),
    CONSTRAINT uq_categoria_nombre UNIQUE (nombre),
    INDEX idx_categoria_activo (activo)
) ENGINE=InnoDB
  DEFAULT CHARSET=utf8mb4
  COLLATE=utf8mb4_unicode_ci
  COMMENT='Categorías del menú digital (ej: Pollos, Bebidas, Guarniciones)';


-- ============================================================
-- TABLA 5: platillo
-- ============================================================
CREATE TABLE IF NOT EXISTS platillo (
    id            INT             NOT NULL AUTO_INCREMENT,
    nombre        VARCHAR(150)    NOT NULL,
    descripcion   TEXT,
    precio        DECIMAL(8, 2)   NOT NULL,
    imagen_url    VARCHAR(500),
    activo        BOOLEAN         NOT NULL DEFAULT TRUE,
    categoria_id  INT             NOT NULL,

    CONSTRAINT pk_platillo PRIMARY KEY (id),
    CONSTRAINT chk_platillo_precio CHECK (precio > 0),
    CONSTRAINT fk_platillo_categoria
        FOREIGN KEY (categoria_id) REFERENCES categoria (id)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,
    INDEX idx_platillo_activo (activo),
    INDEX idx_platillo_categoria (categoria_id),
    INDEX idx_platillo_carta (categoria_id, activo)
) ENGINE=InnoDB
  DEFAULT CHARSET=utf8mb4
  COLLATE=utf8mb4_unicode_ci
  COMMENT='Platillos del menú digital con precio y disponibilidad';


-- ============================================================
-- TABLA 6: pedido_takeaway
-- ============================================================
CREATE TABLE IF NOT EXISTS pedido_takeaway (
    id                  INT           NOT NULL AUTO_INCREMENT,
    cliente_nombre      VARCHAR(100)  NOT NULL,
    cliente_contacto    VARCHAR(20)   NOT NULL,
    total               DECIMAL(10,2) NOT NULL DEFAULT 0.00,
    estado              ENUM('recibido', 'en_preparacion', 'listo', 'entregado', 'cancelado')
                                      NOT NULL DEFAULT 'recibido',
    codigo_seguimiento  VARCHAR(20)   NOT NULL,
    created_at          DATETIME      NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT pk_pedido_takeaway PRIMARY KEY (id),
    CONSTRAINT uq_pedido_codigo UNIQUE (codigo_seguimiento),
    CONSTRAINT chk_pedido_total CHECK (total >= 0),
    INDEX idx_pedido_estado (estado),
    INDEX idx_pedido_fecha (created_at),
    INDEX idx_pedido_codigo (codigo_seguimiento),
    INDEX idx_pedido_fecha_estado (created_at, estado)
) ENGINE=InnoDB
  DEFAULT CHARSET=utf8mb4
  COLLATE=utf8mb4_unicode_ci
  COMMENT='Pedidos para llevar (takeaway) realizados por clientes';


-- ============================================================
-- TABLA 7: detalle_pedido
-- ============================================================
CREATE TABLE IF NOT EXISTS detalle_pedido (
    id               INT           NOT NULL AUTO_INCREMENT,
    pedido_id        INT           NOT NULL,
    platillo_id      INT           NOT NULL,
    cantidad         TINYINT       NOT NULL,
    precio_unitario  DECIMAL(8,2)  NOT NULL,

    CONSTRAINT pk_detalle_pedido PRIMARY KEY (id),
    CONSTRAINT chk_detalle_cantidad CHECK (cantidad >= 1 AND cantidad <= 99),
    CONSTRAINT chk_detalle_precio CHECK (precio_unitario > 0),
    CONSTRAINT fk_detalle_pedido
        FOREIGN KEY (pedido_id) REFERENCES pedido_takeaway (id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    CONSTRAINT fk_detalle_platillo
        FOREIGN KEY (platillo_id) REFERENCES platillo (id)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,
    INDEX idx_detalle_pedido (pedido_id),
    INDEX idx_detalle_platillo (platillo_id)
) ENGINE=InnoDB
  DEFAULT CHARSET=utf8mb4
  COLLATE=utf8mb4_unicode_ci
  COMMENT='Ítems individuales de cada pedido takeaway con precio fijo al momento del pedido';


-- ============================================================
-- TABLA 8: configuracion
-- ============================================================
CREATE TABLE IF NOT EXISTS configuracion (
    id     INT          NOT NULL AUTO_INCREMENT,
    clave  VARCHAR(100) NOT NULL,
    valor  VARCHAR(500) NOT NULL,

    CONSTRAINT pk_configuracion PRIMARY KEY (id),
    CONSTRAINT uq_configuracion_clave UNIQUE (clave)
) ENGINE=InnoDB
  DEFAULT CHARSET=utf8mb4
  COLLATE=utf8mb4_unicode_ci
  COMMENT='Parámetros configurables del sistema modificables desde el panel admin';
```

---

## 4. DATOS SEMILLA (SEED DATA)

```sql
-- ============================================================
-- SEED DATA — Pollería Leña y Carbón
-- Orden: respetar FK (insertar padre antes que hijo)
-- ============================================================

-- -------------------------------------------------------
-- 4.1. Configuración del sistema
-- -------------------------------------------------------
INSERT INTO configuracion (clave, valor) VALUES
    ('nombre_negocio',        'Pollería Leña y Carbón'),
    ('horario_apertura',      '12:00'),
    ('horario_cierre',        '22:00'),
    ('contacto_telefono',     '987654321'),
    ('contacto_email',        'contacto@lenacarbon.com'),
    ('jwt_expiration_hours',  '8'),
    ('max_personas_reserva',  '20'),
    ('bloqueo_reserva_horas', '2'),
    ('cancelacion_min_horas', '1'),
    ('moneda',                'PEN');


-- -------------------------------------------------------
-- 4.2. Usuario administrador inicial
-- Contraseña: Admin123! (hash bcrypt 12 rounds)
-- IMPORTANTE: cambiar en producción
-- -------------------------------------------------------
INSERT INTO usuario (nombre, email, password_hash, rol, activo) VALUES
    (
        'Administrador Principal',
        'admin@lenacarbon.com',
        '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMeSSmmRFIBbKMmkzKlBh3zJAO',
        'ADMIN',
        TRUE
    ),
    (
        'Recepcionista Demo',
        'recepcion@lenacarbon.com',
        '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMeSSmmRFIBbKMmkzKlBh3zJAO',
        'RECEPCIONISTA',
        TRUE
    );


-- -------------------------------------------------------
-- 4.3. Mesas del restaurante
-- -------------------------------------------------------
INSERT INTO mesa (numero, capacidad, tipo_ocasion, activo) VALUES
    -- Mesas familiares (capacidad ≥ 4)
    (1,  4,  'familiar',  TRUE),
    (2,  4,  'familiar',  TRUE),
    (3,  6,  'familiar',  TRUE),
    (4,  6,  'familiar',  TRUE),
    (5,  8,  'familiar',  TRUE),
    (6,  8,  'familiar',  TRUE),
    (7,  10, 'familiar',  TRUE),
    -- Mesas románticas (capacidad = 2)
    (8,  2,  'romantica', TRUE),
    (9,  2,  'romantica', TRUE),
    (10, 2,  'romantica', TRUE),
    -- Mesas para reuniones (capacidad ≥ 6)
    (11, 6,  'reunion',   TRUE),
    (12, 8,  'reunion',   TRUE),
    (13, 10, 'reunion',   TRUE),
    (14, 12, 'reunion',   TRUE);


-- -------------------------------------------------------
-- 4.4. Categorías de la carta
-- -------------------------------------------------------
INSERT INTO categoria (nombre, descripcion, activo) VALUES
    ('Pollos a la Brasa',   'Nuestros pollos preparados a la leña y al carbón con receta tradicional', TRUE),
    ('Guarniciones',        'Papas fritas, ensaladas, cremas y acompañamientos',                       TRUE),
    ('Parrillas',           'Carnes y anticuchos a la brasa',                                           TRUE),
    ('Bebidas',             'Gaseosas, refrescos, jugos naturales y cervezas',                          TRUE),
    ('Postres',             'Helados, tortas y dulces de la casa',                                      TRUE);


-- -------------------------------------------------------
-- 4.5. Platillos de la carta
-- -------------------------------------------------------
INSERT INTO platillo (nombre, descripcion, precio, imagen_url, activo, categoria_id) VALUES
    -- Pollos a la Brasa (categoria_id = 1)
    ('Pollo Entero a la Brasa',
     'Pollo entero preparado a la leña con adobo secreto de la casa. Incluye papas fritas y ensalada.',
     52.00, NULL, TRUE, 1),

    ('1/2 Pollo a la Brasa',
     'Media pieza de pollo a la brasa. Incluye papas fritas y ensalada.',
     28.00, NULL, TRUE, 1),

    ('1/4 Pollo a la Brasa',
     'Cuarto de pollo a la brasa (pierna o pecho). Incluye papas fritas.',
     16.00, NULL, TRUE, 1),

    ('1/4 Pollo + Gaseosa Personal',
     'Cuarto de pollo a la brasa acompañado de una gaseosa personal.',
     20.00, NULL, TRUE, 1),

    -- Guarniciones (categoria_id = 2)
    ('Papas Fritas Porción',
     'Porción generosa de papas fritas crujientes con crema huancaína.',
     8.00,  NULL, TRUE, 2),

    ('Ensalada Mixta',
     'Lechuga, tomate, zanahoria y pepino con aderezo de la casa.',
     6.00,  NULL, TRUE, 2),

    ('Yucas Fritas',
     'Yuca cocida y frita, crujiente por fuera y suave por dentro.',
     7.00,  NULL, TRUE, 2),

    ('Crema Huancaína',
     'Salsa de ají amarillo con queso fresco. Porción para compartir.',
     4.00,  NULL, TRUE, 2),

    -- Parrillas (categoria_id = 3)
    ('Anticuchos de Corazón x6',
     'Seis pinchos de corazón de res marinados y asados a la brasa. Incluye papas sancochadas y choclo.',
     22.00, NULL, TRUE, 3),

    ('Parrilla Mixta Personal',
     'Combinación de pollo, costilla y chorizo a la brasa. Incluye guarnición a elección.',
     35.00, NULL, TRUE, 3),

    ('Chuleta a la Brasa',
     'Chuleta de cerdo adobada y asada al carbón. Incluye papas fritas.',
     28.00, NULL, TRUE, 3),

    -- Bebidas (categoria_id = 4)
    ('Gaseosa Personal 300ml',
     'Coca-Cola, Inca Kola, Sprite o Fanta en presentación personal.',
     4.00,  NULL, TRUE, 4),

    ('Gaseosa Familiar 1.5L',
     'Coca-Cola, Inca Kola o Sprite en botella familiar.',
     10.00, NULL, TRUE, 4),

    ('Chicha Morada Jarra',
     'Chicha morada preparada en casa con maíz morado, piña y canela.',
     12.00, NULL, TRUE, 4),

    ('Jugo Natural Vaso',
     'Jugo de maracuyá, naranja, piña o papaya recién preparado.',
     6.00,  NULL, TRUE, 4),

    ('Cerveza Nacional 330ml',
     'Cristal o Pilsen Callao en lata o botella.',
     7.00,  NULL, TRUE, 4),

    -- Postres (categoria_id = 5)
    ('Helado de Lúcuma',
     'Helado artesanal de lúcuma peruana. Una bola.',
     5.00,  NULL, TRUE, 5),

    ('Mazamorra Morada',
     'Postre tradicional peruano de maíz morado con frutas.',
     6.00,  NULL, TRUE, 5);
```

---

## 5. MODELOS SQLALCHEMY (Python)

```python
# app/extensions.py
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_marshmallow import Marshmallow

db  = SQLAlchemy()
jwt = JWTManager()
ma  = Marshmallow()
```

```python
# app/models/usuario.py
from app.extensions import db
import bcrypt
from datetime import datetime

class Usuario(db.Model):
    __tablename__ = 'usuario'

    id            = db.Column(db.Integer, primary_key=True)
    nombre        = db.Column(db.String(100), nullable=False)
    email         = db.Column(db.String(150), nullable=False, unique=True)
    password_hash = db.Column(db.String(255), nullable=False)
    rol           = db.Column(db.Enum('ADMIN', 'RECEPCIONISTA'), nullable=False,
                              default='RECEPCIONISTA')
    activo        = db.Column(db.Boolean, nullable=False, default=True)
    created_at    = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def set_password(self, password: str) -> None:
        """Hashea la contraseña con bcrypt (12 rounds) y la almacena."""
        self.password_hash = bcrypt.hashpw(
            password.encode('utf-8'),
            bcrypt.gensalt(rounds=12)
        ).decode('utf-8')

    def check_password(self, password: str) -> bool:
        """Verifica la contraseña contra el hash almacenado."""
        return bcrypt.checkpw(
            password.encode('utf-8'),
            self.password_hash.encode('utf-8')
        )

    def to_dict(self) -> dict:
        return {
            'id':         self.id,
            'nombre':     self.nombre,
            'email':      self.email,
            'rol':        self.rol,
            'activo':     self.activo,
            'created_at': self.created_at.isoformat()
        }

    def __repr__(self) -> str:
        return f'<Usuario {self.email} [{self.rol}]>'
```

```python
# app/models/mesa.py
from app.extensions import db

class Mesa(db.Model):
    __tablename__ = 'mesa'

    id           = db.Column(db.Integer, primary_key=True)
    numero       = db.Column(db.Integer, nullable=False, unique=True)
    capacidad    = db.Column(db.SmallInteger, nullable=False)
    tipo_ocasion = db.Column(
        db.Enum('familiar', 'romantica', 'reunion'),
        nullable=False
    )
    activo       = db.Column(db.Boolean, nullable=False, default=True)

    # Relación inversa: una mesa puede tener muchas reservas
    reservas     = db.relationship('Reserva', backref='mesa', lazy='dynamic')

    def to_dict(self) -> dict:
        return {
            'id':           self.id,
            'numero':       self.numero,
            'capacidad':    self.capacidad,
            'tipo_ocasion': self.tipo_ocasion,
            'activo':       self.activo
        }

    def __repr__(self) -> str:
        return f'<Mesa #{self.numero} [{self.tipo_ocasion}] cap={self.capacidad}>'
```

```python
# app/models/reserva.py
from app.extensions import db
from datetime import datetime
import secrets
import string

class Reserva(db.Model):
    __tablename__ = 'reserva'

    id                  = db.Column(db.Integer, primary_key=True)
    cliente_nombre      = db.Column(db.String(100), nullable=False)
    cliente_contacto    = db.Column(db.String(20), nullable=False)
    fecha               = db.Column(db.Date, nullable=False)
    hora                = db.Column(db.Time, nullable=False)
    num_personas        = db.Column(db.SmallInteger, nullable=False)
    tipo_ocasion        = db.Column(
        db.Enum('familiar', 'romantica', 'reunion'),
        nullable=False
    )
    estado              = db.Column(
        db.Enum('pendiente', 'confirmada', 'completada', 'cancelada'),
        nullable=False,
        default='pendiente'
    )
    codigo_confirmacion = db.Column(db.String(20), nullable=False, unique=True)
    mesa_id             = db.Column(db.Integer, db.ForeignKey('mesa.id',
                                    ondelete='RESTRICT'), nullable=False)
    created_at          = db.Column(db.DateTime, nullable=False,
                                    default=datetime.utcnow)

    # Transiciones de estado válidas
    TRANSICIONES_VALIDAS = {
        'pendiente':   ['confirmada', 'cancelada'],
        'confirmada':  ['completada', 'cancelada'],
        'completada':  [],
        'cancelada':   [],
    }

    @staticmethod
    def generar_codigo() -> str:
        """Genera un código de confirmación único con formato POLL-XXXXXX."""
        caracteres = string.ascii_uppercase + string.digits
        sufijo = ''.join(secrets.choice(caracteres) for _ in range(6))
        return f'POLL-{sufijo}'

    def puede_transicionar(self, nuevo_estado: str) -> bool:
        """Valida si la transición de estado es permitida."""
        return nuevo_estado in self.TRANSICIONES_VALIDAS.get(self.estado, [])

    def to_dict(self) -> dict:
        return {
            'id':                  self.id,
            'cliente_nombre':      self.cliente_nombre,
            'cliente_contacto':    self.cliente_contacto,
            'fecha':               self.fecha.isoformat(),
            'hora':                str(self.hora),
            'num_personas':        self.num_personas,
            'tipo_ocasion':        self.tipo_ocasion,
            'estado':              self.estado,
            'codigo_confirmacion': self.codigo_confirmacion,
            'mesa_id':             self.mesa_id,
            'created_at':          self.created_at.isoformat()
        }

    def __repr__(self) -> str:
        return f'<Reserva {self.codigo_confirmacion} [{self.estado}]>'
```

```python
# app/models/categoria.py
from app.extensions import db

class Categoria(db.Model):
    __tablename__ = 'categoria'

    id          = db.Column(db.Integer, primary_key=True)
    nombre      = db.Column(db.String(100), nullable=False, unique=True)
    descripcion = db.Column(db.Text)
    activo      = db.Column(db.Boolean, nullable=False, default=True)

    # Relación inversa
    platillos   = db.relationship('Platillo', backref='categoria', lazy='dynamic')

    def to_dict(self, include_platillos: bool = False) -> dict:
        data = {
            'id':          self.id,
            'nombre':      self.nombre,
            'descripcion': self.descripcion,
            'activo':      self.activo
        }
        if include_platillos:
            data['platillos'] = [p.to_dict() for p in
                                 self.platillos.filter_by(activo=True).all()]
        return data

    def __repr__(self) -> str:
        return f'<Categoria {self.nombre}>'
```

```python
# app/models/platillo.py
from app.extensions import db

class Platillo(db.Model):
    __tablename__ = 'platillo'

    id           = db.Column(db.Integer, primary_key=True)
    nombre       = db.Column(db.String(150), nullable=False)
    descripcion  = db.Column(db.Text)
    precio       = db.Column(db.Numeric(8, 2), nullable=False)
    imagen_url   = db.Column(db.String(500))
    activo       = db.Column(db.Boolean, nullable=False, default=True)
    categoria_id = db.Column(db.Integer, db.ForeignKey('categoria.id',
                             ondelete='RESTRICT'), nullable=False)

    # Relación inversa
    detalles     = db.relationship('DetallePedido', backref='platillo', lazy='dynamic')

    def to_dict(self) -> dict:
        return {
            'id':           self.id,
            'nombre':       self.nombre,
            'descripcion':  self.descripcion,
            'precio':       float(self.precio),
            'imagen_url':   self.imagen_url,
            'activo':       self.activo,
            'categoria_id': self.categoria_id,
            'categoria':    self.categoria.nombre if self.categoria else None
        }

    def __repr__(self) -> str:
        return f'<Platillo {self.nombre} S/{self.precio}>'
```

```python
# app/models/pedido_takeaway.py
from app.extensions import db
from datetime import datetime
import secrets
import string

class PedidoTakeaway(db.Model):
    __tablename__ = 'pedido_takeaway'

    id                 = db.Column(db.Integer, primary_key=True)
    cliente_nombre     = db.Column(db.String(100), nullable=False)
    cliente_contacto   = db.Column(db.String(20), nullable=False)
    total              = db.Column(db.Numeric(10, 2), nullable=False, default=0.00)
    estado             = db.Column(
        db.Enum('recibido', 'en_preparacion', 'listo', 'entregado', 'cancelado'),
        nullable=False,
        default='recibido'
    )
    codigo_seguimiento = db.Column(db.String(20), nullable=False, unique=True)
    created_at         = db.Column(db.DateTime, nullable=False,
                                   default=datetime.utcnow)

    # Relación 1:N con ítems del pedido
    detalles           = db.relationship('DetallePedido', backref='pedido',
                                         lazy='joined', cascade='all, delete-orphan')

    # Transiciones de estado válidas (RN-05)
    TRANSICIONES_VALIDAS = {
        'recibido':       ['en_preparacion', 'cancelado'],
        'en_preparacion': ['listo'],
        'listo':          ['entregado'],
        'entregado':      [],
        'cancelado':      [],
    }

    @staticmethod
    def generar_codigo() -> str:
        """Genera un código de seguimiento único con formato TW-XXXXXXXX."""
        caracteres = string.ascii_uppercase + string.digits
        sufijo = ''.join(secrets.choice(caracteres) for _ in range(8))
        return f'TW-{sufijo}'

    def puede_transicionar(self, nuevo_estado: str) -> bool:
        """Valida si la transición de estado es permitida (RN-05)."""
        return nuevo_estado in self.TRANSICIONES_VALIDAS.get(self.estado, [])

    def to_dict(self, include_detalles: bool = True) -> dict:
        data = {
            'id':                 self.id,
            'cliente_nombre':     self.cliente_nombre,
            'cliente_contacto':   self.cliente_contacto,
            'total':              float(self.total),
            'estado':             self.estado,
            'codigo_seguimiento': self.codigo_seguimiento,
            'created_at':         self.created_at.isoformat()
        }
        if include_detalles:
            data['items'] = [d.to_dict() for d in self.detalles]
        return data

    def __repr__(self) -> str:
        return f'<PedidoTakeaway {self.codigo_seguimiento} [{self.estado}]>'
```

```python
# app/models/detalle_pedido.py
from app.extensions import db

class DetallePedido(db.Model):
    __tablename__ = 'detalle_pedido'

    id              = db.Column(db.Integer, primary_key=True)
    pedido_id       = db.Column(db.Integer, db.ForeignKey('pedido_takeaway.id',
                                ondelete='CASCADE'), nullable=False)
    platillo_id     = db.Column(db.Integer, db.ForeignKey('platillo.id',
                                ondelete='RESTRICT'), nullable=False)
    cantidad        = db.Column(db.SmallInteger, nullable=False)
    precio_unitario = db.Column(db.Numeric(8, 2), nullable=False)

    @property
    def subtotal(self) -> float:
        """Calcula el subtotal del ítem (cantidad × precio unitario)."""
        return float(self.cantidad) * float(self.precio_unitario)

    def to_dict(self) -> dict:
        return {
            'id':              self.id,
            'platillo_id':     self.platillo_id,
            'platillo_nombre': self.platillo.nombre if self.platillo else None,
            'cantidad':        self.cantidad,
            'precio_unitario': float(self.precio_unitario),
            'subtotal':        self.subtotal
        }

    def __repr__(self) -> str:
        return f'<DetallePedido pedido={self.pedido_id} platillo={self.platillo_id} x{self.cantidad}>'
```

```python
# app/models/configuracion.py
from app.extensions import db

class Configuracion(db.Model):
    __tablename__ = 'configuracion'

    id    = db.Column(db.Integer, primary_key=True)
    clave = db.Column(db.String(100), nullable=False, unique=True)
    valor = db.Column(db.String(500), nullable=False)

    # Claves permitidas (validación en service layer)
    CLAVES_PERMITIDAS = {
        'nombre_negocio',
        'horario_apertura',
        'horario_cierre',
        'contacto_telefono',
        'contacto_email',
        'jwt_expiration_hours',
        'max_personas_reserva',
        'bloqueo_reserva_horas',
        'cancelacion_min_horas',
        'moneda',
    }

    @classmethod
    def get_valor(cls, clave: str, default=None):
        """Obtiene el valor de una clave de configuración."""
        config = cls.query.filter_by(clave=clave).first()
        return config.valor if config else default

    @classmethod
    def get_all_dict(cls) -> dict:
        """Retorna toda la configuración como diccionario clave:valor."""
        return {c.clave: c.valor for c in cls.query.all()}

    def to_dict(self) -> dict:
        return {'clave': self.clave, 'valor': self.valor}

    def __repr__(self) -> str:
        return f'<Configuracion {self.clave}={self.valor}>'
```

---

## 6. CONSULTAS SQL CRÍTICAS DEL NEGOCIO

Las siguientes consultas implementan la lógica de negocio más importante del sistema. Sirven como referencia directa para la implementación en la capa `services/`.

### 6.1. Asignación automática de mesa (RN-01, RN-02, RN-03)

```sql
-- Encuentra la mesa más adecuada disponible para una reserva
-- Parámetros: :fecha, :hora_inicio, :hora_fin (hora + 2h bloqueo),
--             :tipo_ocasion, :num_personas

SELECT
    m.id,
    m.numero,
    m.capacidad,
    m.tipo_ocasion
FROM mesa m
WHERE
    -- La mesa debe estar activa
    m.activo = TRUE

    -- Debe ser del tipo de ocasión solicitado
    AND m.tipo_ocasion = :tipo_ocasion

    -- Debe tener capacidad suficiente
    AND m.capacidad >= :num_personas

    -- No debe tener reserva activa que se solape con el bloqueo de 2 horas
    AND m.id NOT IN (
        SELECT r.mesa_id
        FROM reserva r
        WHERE
            r.fecha    = :fecha
            AND r.estado NOT IN ('cancelada', 'completada')
            AND (
                -- El bloqueo existente se solapa con la nueva reserva
                r.hora < :hora_fin
                AND ADDTIME(r.hora, '02:00:00') > :hora_inicio
            )
    )

-- Prioridad: menor capacidad que cumpla el mínimo (mesa más ajustada)
ORDER BY m.capacidad ASC

LIMIT 1;
```

### 6.2. Verificar disponibilidad de una mesa específica (RN-01)

```sql
-- Verifica si una mesa específica tiene conflicto de horario
-- Retorna 1 si hay conflicto, 0 si está libre

SELECT COUNT(*) AS tiene_conflicto
FROM reserva r
WHERE
    r.mesa_id = :mesa_id
    AND r.fecha = :fecha
    AND r.estado NOT IN ('cancelada', 'completada')
    AND r.hora < ADDTIME(:hora, '02:00:00')
    AND ADDTIME(r.hora, '02:00:00') > :hora;
```

### 6.3. Listar reservas del día con datos de mesa (RF-05)

```sql
-- Lista todas las reservas de una fecha con información de mesa
SELECT
    r.id,
    r.cliente_nombre,
    r.cliente_contacto,
    r.hora,
    r.num_personas,
    r.tipo_ocasion,
    r.estado,
    r.codigo_confirmacion,
    m.numero   AS mesa_numero,
    m.capacidad AS mesa_capacidad
FROM reserva r
INNER JOIN mesa m ON r.mesa_id = m.id
WHERE r.fecha = :fecha
ORDER BY r.hora ASC, r.estado ASC;
```

### 6.4. Carta digital pública: categorías con platillos activos (RF-09)

```sql
-- Retorna todas las categorías activas con sus platillos activos anidados
SELECT
    c.id          AS categoria_id,
    c.nombre      AS categoria_nombre,
    c.descripcion AS categoria_descripcion,
    p.id          AS platillo_id,
    p.nombre      AS platillo_nombre,
    p.descripcion AS platillo_descripcion,
    p.precio,
    p.imagen_url
FROM categoria c
LEFT JOIN platillo p
    ON p.categoria_id = c.id
    AND p.activo = TRUE
WHERE c.activo = TRUE
ORDER BY c.id ASC, p.nombre ASC;
```

### 6.5. Calcular total de un pedido takeaway (RN-06)

```sql
-- Calcula el total de un pedido a partir de sus ítems
-- (precio fijado en el momento del pedido, no el precio actual del platillo)
SELECT
    SUM(dp.cantidad * dp.precio_unitario) AS total
FROM detalle_pedido dp
WHERE dp.pedido_id = :pedido_id;
```

### 6.6. Dashboard del administrador (RF-21)

```sql
-- Métricas del día para el panel de administración
SELECT
    -- Total de reservas del día
    (SELECT COUNT(*)
     FROM reserva
     WHERE fecha = CURDATE()
       AND estado != 'cancelada') AS reservas_hoy,

    -- Total de pedidos takeaway del día
    (SELECT COUNT(*)
     FROM pedido_takeaway
     WHERE DATE(created_at) = CURDATE()
       AND estado != 'cancelado') AS pedidos_hoy,

    -- Ingresos estimados del día (pedidos no cancelados)
    (SELECT COALESCE(SUM(total), 0)
     FROM pedido_takeaway
     WHERE DATE(created_at) = CURDATE()
       AND estado NOT IN ('cancelado', 'recibido')) AS ingresos_estimados;

-- Top 5 platillos más pedidos (histórico)
SELECT
    p.nombre,
    SUM(dp.cantidad) AS total_pedido
FROM detalle_pedido dp
INNER JOIN platillo p ON dp.platillo_id = p.id
INNER JOIN pedido_takeaway pt ON dp.pedido_id = pt.id
WHERE pt.estado != 'cancelado'
  AND DATE(pt.created_at) = CURDATE()
GROUP BY p.id, p.nombre
ORDER BY total_pedido DESC
LIMIT 5;
```

### 6.7. Validar cancelación de reserva por código (RF-07)

```sql
-- Busca una reserva por código y valida que se pueda cancelar
SELECT
    r.id,
    r.estado,
    r.fecha,
    r.hora,
    TIMESTAMPDIFF(
        MINUTE,
        NOW(),
        TIMESTAMP(r.fecha, r.hora)
    ) AS minutos_hasta_reserva
FROM reserva r
WHERE r.codigo_confirmacion = :codigo
LIMIT 1;
-- La cancelación es válida si:
-- estado IN ('pendiente', 'confirmada') AND minutos_hasta_reserva >= 60
```

### 6.8. Historial de pedidos con filtros (RF-24)

```sql
-- Historial de pedidos takeaway con filtros opcionales
SELECT
    pt.id,
    pt.cliente_nombre,
    pt.cliente_contacto,
    pt.total,
    pt.estado,
    pt.codigo_seguimiento,
    pt.created_at,
    COUNT(dp.id) AS num_items
FROM pedido_takeaway pt
LEFT JOIN detalle_pedido dp ON dp.pedido_id = pt.id
WHERE
    (:fecha     IS NULL OR DATE(pt.created_at) = :fecha)
    AND (:estado IS NULL OR pt.estado = :estado)
GROUP BY pt.id
ORDER BY pt.created_at DESC;
```

---

## 7. ÍNDICES Y JUSTIFICACIÓN

| Tabla | Índice | Columnas | Tipo | Justificación |
|-------|--------|----------|------|---------------|
| `usuario` | `uq_usuario_email` | `email` | UNIQUE | Garantiza unicidad de email para login; búsqueda O(log n) |
| `usuario` | `idx_usuario_activo` | `activo` | INDEX | Filtro frecuente al validar cuentas activas en login |
| `mesa` | `uq_mesa_numero` | `numero` | UNIQUE | Evita mesas con número duplicado |
| `mesa` | `idx_mesa_disponibilidad` | `activo, tipo_ocasion, capacidad` | INDEX compuesto | Optimiza la consulta de asignación automática (sección 6.1) |
| `reserva` | `uq_reserva_codigo` | `codigo_confirmacion` | UNIQUE | Búsqueda directa por código de confirmación; garantiza unicidad |
| `reserva` | `idx_reserva_mesa_fecha` | `mesa_id, fecha, hora` | INDEX compuesto | Optimiza la validación de conflictos de horario por mesa (sección 6.2) |
| `reserva` | `idx_reserva_fecha_estado` | `fecha, estado` | INDEX compuesto | Listado de reservas del día con filtro de estado (sección 6.3) |
| `platillo` | `idx_platillo_carta` | `categoria_id, activo` | INDEX compuesto | Optimiza la carga de la carta pública (sección 6.4) |
| `pedido_takeaway` | `uq_pedido_codigo` | `codigo_seguimiento` | UNIQUE | Búsqueda por código de seguimiento; garantiza unicidad |
| `pedido_takeaway` | `idx_pedido_fecha_estado` | `created_at, estado` | INDEX compuesto | Listado de pedidos del día con filtro de estado |
| `detalle_pedido` | `idx_detalle_pedido` | `pedido_id` | INDEX | JOIN frecuente al cargar los ítems de un pedido |
| `configuracion` | `uq_configuracion_clave` | `clave` | UNIQUE | Acceso O(1) por clave de configuración |

---

## 8. PROCEDIMIENTOS PARA GESTIÓN DE LA BD

### 8.1. Crear base de datos de prueba (para pytest)

```sql
-- Base de datos exclusiva para pruebas de integración (no usar en producción)
CREATE DATABASE IF NOT EXISTS polleria_test
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

-- Usuario con permisos solo sobre la BD de prueba
CREATE USER IF NOT EXISTS 'polleria_test_user'@'localhost'
    IDENTIFIED BY 'test_password_local';

GRANT ALL PRIVILEGES ON polleria_test.* TO 'polleria_test_user'@'localhost';
FLUSH PRIVILEGES;
```

### 8.2. Script de inicialización completa (desarrollo)

```bash
# Desde la raíz del proyecto backend
# 1. Crear las tablas vía Flask-SQLAlchemy
flask shell -c "from app.extensions import db; from app import create_app; app = create_app('development'); app.app_context().push(); db.create_all(); print('Tablas creadas OK')"

# 2. Ejecutar el seed data
mysql -u root -p polleria_lena_carbon < .kiro/specs/seed_data.sql

# 3. Verificar
mysql -u root -p polleria_lena_carbon -e "SHOW TABLES; SELECT COUNT(*) FROM platillo; SELECT COUNT(*) FROM mesa;"
```

### 8.3. Script de reset para tests

```python
# tests/conftest.py — fixture de reset de BD para pytest
@pytest.fixture(scope='function')
def app():
    """Crea una app Flask con BD SQLite en memoria para cada test."""
    from app import create_app
    from app.extensions import db as _db

    _app = create_app('testing')
    with _app.app_context():
        _db.create_all()         # Crear todas las tablas
        _seed_test_data(_db)     # Insertar datos mínimos de prueba
        yield _app
        _db.session.remove()
        _db.drop_all()           # Limpiar completamente

def _seed_test_data(db):
    """Inserta datos mínimos necesarios para las pruebas unitarias."""
    from app.models.usuario import Usuario
    from app.models.mesa import Mesa
    from app.models.categoria import Categoria
    from app.models.configuracion import Configuracion

    # Usuario admin de prueba
    admin = Usuario(nombre='Admin Test', email='admin@test.com',
                    rol='ADMIN', activo=True)
    admin.set_password('Test1234!')
    db.session.add(admin)

    # Mesas de prueba
    mesas = [
        Mesa(numero=1, capacidad=4, tipo_ocasion='familiar',  activo=True),
        Mesa(numero=2, capacidad=2, tipo_ocasion='romantica', activo=True),
        Mesa(numero=3, capacidad=8, tipo_ocasion='reunion',   activo=True),
    ]
    db.session.bulk_save_objects(mesas)

    # Categoría y configuración de prueba
    cat = Categoria(nombre='Pollos Test', descripcion='Prueba', activo=True)
    cfg = Configuracion(clave='bloqueo_reserva_horas', valor='2')
    db.session.add_all([cat, cfg])
    db.session.commit()
```

---

## 9. DIAGRAMA DE ESTADOS DE ENTIDADES

### 9.1. Estados de Reserva

```
                    ┌─────────────┐
         ┌─────────▶│  pendiente  │◀──────────────┐
         │           └──────┬──────┘               │
         │                  │ confirmar            │ (no aplica
         │                  ▼                      │  retroceso)
         │           ┌─────────────┐               │
cancelar │           │  confirmada │               │
(desde   │           └──────┬──────┘               │
cualquier│                  │ completar            │
estado   │                  ▼                      │
activo)  │           ┌─────────────┐               │
         │           │  completada │ (estado final) │
         │           └─────────────┘               │
         │                                         │
         └────────────────────────────────────────▶│
                                                   │
                     ┌─────────────┐               │
                     │  cancelada  │◀──────────────┘
                     └─────────────┘  (estado final)
```

### 9.2. Estados de Pedido Takeaway (RN-05)

```
                ┌──────────────────────────────────────┐
                │                                      │ cancelar
                ▼                                      │ (SOLO desde
         ┌────────────┐    ┌────────────────┐          │ 'recibido')
         │  recibido  │───▶│ en_preparacion │          │
         └────────────┘    └───────┬────────┘          │
                │                  │                   │
                │ cancelar         ▼                   │
                │           ┌────────────┐             │
                │           │    listo   │             │
                │           └─────┬──────┘             │
                │                 │                    │
                ▼                 ▼                    │
         ┌────────────┐    ┌────────────┐             │
         │  cancelado │    │  entregado │             │
         │ (terminal) │    │ (terminal) │             │
         └────────────┘    └────────────┘             │
                ▲                                      │
                └──────────────────────────────────────┘
```

---

## 10. REFERENCIA RÁPIDA DE TABLAS

| Tabla | Filas estimadas | Lecturas | Escrituras | Índices críticos |
|-------|----------------|----------|------------|-----------------|
| `usuario` | ~10 | Baja | Muy baja | `email` (UNIQUE) |
| `mesa` | ~15 | Alta | Muy baja | `tipo_ocasion, capacidad, activo` |
| `reserva` | ~5,000/año | Alta | Media | `fecha`, `mesa_id + fecha + hora` |
| `categoria` | ~10 | Alta | Muy baja | `activo` |
| `platillo` | ~30 | Muy alta | Baja | `categoria_id + activo` |
| `pedido_takeaway` | ~8,000/año | Alta | Media | `created_at + estado` |
| `detalle_pedido` | ~25,000/año | Alta | Media | `pedido_id` |
| `configuracion` | ~10 | Media | Muy baja | `clave` (UNIQUE) |

---

## 11. HISTORIAL DE VERSIONES

| Versión | Fecha | Descripción |
|---------|-------|-------------|
| 1.0.0 | Junio 2026 | Versión inicial — DDL completo, 8 modelos SQLAlchemy, seed data, 8 consultas SQL críticas |

---

*Documento generado como parte de la metodología Spec Driven Development (SDD) para el proyecto académico IS-489 — UNSCH 2026. Este archivo es la fuente de verdad para la estructura de datos del sistema y debe mantenerse sincronizado con los modelos SQLAlchemy durante toda la fase de implementación.*
