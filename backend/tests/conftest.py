# =============================================================================
# backend/tests/conftest.py
# Configuración global de pytest — Pollería Leña y Carbón
# IS-489 Pruebas y Aseguramiento de Calidad — UNSCH 2026
# =============================================================================

import pytest
from datetime import date, timedelta

from app import create_app
from app.extensions import db as _db
from app.models.usuario import Usuario
from app.models.mesa import Mesa
from app.models.categoria import Categoria
from app.models.platillo import Platillo
from app.models.reserva import Reserva
from app.models.pedido_takeaway import PedidoTakeaway
from app.models.detalle_pedido import DetallePedido
from flask_jwt_extended import create_access_token
from datetime import date, time, timedelta

# ---------------------------------------------------------------------------
# Fixture principal — BD se recrea por cada prueba
# ---------------------------------------------------------------------------


@pytest.fixture(scope="function")
def app():
    """Crea la app Flask con BD SQLite en memoria por cada prueba."""
    aplicacion = create_app("testing")
    with aplicacion.app_context():
        _db.create_all()
        yield aplicacion
        _db.session.remove()
        _db.drop_all()


@pytest.fixture(scope="function")
def db(app):
    """Provee acceso a la BD limpia por cada prueba."""
    return _db


@pytest.fixture(scope="function")
def session(db):
    """Provee la sesión de BD para cada prueba."""
    yield db.session
    db.session.remove()


# ---------------------------------------------------------------------------
# Fixture del cliente HTTP
# ---------------------------------------------------------------------------


@pytest.fixture(scope="function")
def client(app):
    """Cliente HTTP de prueba para endpoints REST."""
    with app.test_client() as cliente:
        yield cliente


# ---------------------------------------------------------------------------
# Fixtures de usuarios
# ---------------------------------------------------------------------------


@pytest.fixture(scope="function")
def usuario_admin(app, session):
    """Crea un usuario administrador en la BD de prueba."""
    with app.app_context():
        admin = Usuario(
            nombre="Admin Prueba", email="admin@prueba.com", rol="ADMIN", activo=True
        )
        admin.set_password("Admin123!")
        session.add(admin)
        session.commit()
        return admin


@pytest.fixture(scope="function")
def usuario_recepcionista(app, session):
    """Crea un usuario recepcionista en la BD de prueba."""
    with app.app_context():
        recep = Usuario(
            nombre="Recep Prueba",
            email="recep@prueba.com",
            rol="RECEPCIONISTA",
            activo=True,
        )
        recep.set_password("Recep123!")
        session.add(recep)
        session.commit()
        return recep


@pytest.fixture(scope="function")
def usuario_inactivo(app, session):
    """Crea un usuario inactivo para probar cuenta desactivada."""
    with app.app_context():
        usuario = Usuario(
            nombre="Usuario Inactivo",
            email="inactivo@prueba.com",
            rol="RECEPCIONISTA",
            activo=False,
        )
        usuario.set_password("Pass123!")
        session.add(usuario)
        session.commit()
        return usuario


# ---------------------------------------------------------------------------
# Fixtures de mesas — retornan objeto simple con ID guardado
# ---------------------------------------------------------------------------


@pytest.fixture(scope="function")
def mesa_familiar(app, session):
    """Crea una mesa familiar con capacidad 6."""
    with app.app_context():
        mesa = Mesa(numero=1, capacidad=6, tipo_ocasion="familiar", activo=True)
        session.add(mesa)
        session.commit()
        mesa_id = mesa.id
    # Retornar objeto simple para evitar DetachedInstanceError
    obj = type(
        "MesaSimple",
        (),
        {
            "id": mesa_id,
            "numero": 1,
            "capacidad": 6,
            "tipo_ocasion": "familiar",
            "activo": True,
        },
    )()
    return obj


@pytest.fixture(scope="function")
def mesa_romantica(app, session):
    """Crea una mesa romántica con capacidad 2."""
    with app.app_context():
        mesa = Mesa(numero=2, capacidad=2, tipo_ocasion="romantica", activo=True)
        session.add(mesa)
        session.commit()
        mesa_id = mesa.id
    obj = type(
        "MesaSimple",
        (),
        {
            "id": mesa_id,
            "numero": 2,
            "capacidad": 2,
            "tipo_ocasion": "romantica",
            "activo": True,
        },
    )()
    return obj


@pytest.fixture(scope="function")
def mesa_reunion(app, session):
    """Crea una mesa de reunión con capacidad 10."""
    with app.app_context():
        mesa = Mesa(numero=3, capacidad=10, tipo_ocasion="reunion", activo=True)
        session.add(mesa)
        session.commit()
        mesa_id = mesa.id
    obj = type(
        "MesaSimple",
        (),
        {
            "id": mesa_id,
            "numero": 3,
            "capacidad": 10,
            "tipo_ocasion": "reunion",
            "activo": True,
        },
    )()
    return obj


# ---------------------------------------------------------------------------
# Fixtures de carta digital
# ---------------------------------------------------------------------------


@pytest.fixture(scope="function")
def categoria_pollos(app, session):
    """Crea una categoría de pollos a la brasa."""
    with app.app_context():
        categoria = Categoria(
            nombre="Pollos a la Brasa",
            descripcion="Pollos preparados a la leña",
            activo=True,
        )
        session.add(categoria)
        session.commit()
        cat_id = categoria.id
    obj = type(
        "CatSimple", (), {"id": cat_id, "nombre": "Pollos a la Brasa", "activo": True}
    )()
    return obj


@pytest.fixture(scope="function")
def platillo_visible(app, session, categoria_pollos):
    """Crea un platillo visible con precio 38.50."""
    with app.app_context():
        platillo = Platillo(
            nombre="1/4 Pollo a la Brasa",
            descripcion="Cuarto de pollo con papas fritas",
            precio=38.50,
            activo=True,
            categoria_id=categoria_pollos.id,
        )
        session.add(platillo)
        session.commit()
        plat_id = platillo.id
    obj = type(
        "PlatSimple",
        (),
        {
            "id": plat_id,
            "nombre": "1/4 Pollo a la Brasa",
            "precio": 38.50,
            "activo": True,
        },
    )()
    return obj


@pytest.fixture(scope="function")
def platillo_oculto(app, session, categoria_pollos):
    """Crea un platillo oculto (activo=False)."""
    with app.app_context():
        platillo = Platillo(
            nombre="Promoción Interna",
            descripcion="Solo para admin",
            precio=25.00,
            activo=False,
            categoria_id=categoria_pollos.id,
        )
        session.add(platillo)
        session.commit()
        plat_id = platillo.id
    obj = type(
        "PlatSimple",
        (),
        {
            "id": plat_id,
            "nombre": "Promoción Interna",
            "precio": 25.00,
            "activo": False,
        },
    )()
    return obj


# ---------------------------------------------------------------------------
# Fixtures de reservas
# ---------------------------------------------------------------------------


@pytest.fixture(scope="function")
def reserva_pendiente(app, session, mesa_familiar):
    """Crea una reserva en estado pendiente para mañana."""
    with app.app_context():
        reserva = Reserva(
            cliente_nombre="Carlos Quispe",
            cliente_contacto="987111222",
            fecha=date.today() + timedelta(days=1),
            hora=time(19, 0),
            num_personas=4,
            tipo_ocasion="familiar",
            estado="pendiente",
            codigo_confirmacion="POLL-TEST1",
            mesa_id=mesa_familiar.id,
        )
        session.add(reserva)
        session.commit()
        res_id = reserva.id
    obj = type(
        "ResSimple",
        (),
        {"id": res_id, "codigo_confirmacion": "POLL-TEST1", "estado": "pendiente"},
    )()
    return obj


# ---------------------------------------------------------------------------
# Fixtures de takeaway
# ---------------------------------------------------------------------------


@pytest.fixture(scope="function")
def pedido_takeaway(app, session):
    """Crea un pedido takeaway en estado recibido."""
    with app.app_context():
        pedido = PedidoTakeaway(
            cliente_nombre="Juan Pérez",
            cliente_contacto="987654321",
            total=77.00,
            estado="recibido",
            codigo_seguimiento="TW-TEST001",
        )
        session.add(pedido)
        session.commit()
        ped_id = pedido.id
    obj = type(
        "PedSimple",
        (),
        {
            "id": ped_id,
            "codigo_seguimiento": "TW-TEST001",
            "estado": "recibido",
            "total": 77.00,
        },
    )()
    return obj


@pytest.fixture(scope="function")
def detalle_pedido(app, session, pedido_takeaway, platillo_visible):
    """Crea un detalle: 2 × 38.50 = 77.00."""
    with app.app_context():
        detalle = DetallePedido(
            pedido_id=pedido_takeaway.id,
            platillo_id=platillo_visible.id,
            cantidad=2,
            precio_unitario=38.50,
        )
        session.add(detalle)
        session.commit()
        det_id = detalle.id
    obj = type(
        "DetSimple", (), {"id": det_id, "cantidad": 2, "precio_unitario": 38.50}
    )()
    return obj


# ---------------------------------------------------------------------------
# Fixtures de tokens JWT
# ---------------------------------------------------------------------------


@pytest.fixture(scope="function")
def token_admin(app, usuario_admin):
    """Genera token JWT para el administrador."""
    with app.app_context():
        from app.models.usuario import Usuario

        admin = Usuario.query.filter_by(email="admin@prueba.com").first()
        token = create_access_token(
            identity=str(admin.id),
            additional_claims={
                "user_id": admin.id,
                "email": admin.email,
                "rol": admin.rol,
            },
        )
        return {"Authorization": f"Bearer {token}"}


@pytest.fixture(scope="function")
def token_recepcionista(app, usuario_recepcionista):
    """Genera token JWT para el recepcionista."""
    with app.app_context():
        from app.models.usuario import Usuario

        recep = Usuario.query.filter_by(email="recep@prueba.com").first()
        token = create_access_token(
            identity=str(recep.id),
            additional_claims={
                "user_id": recep.id,
                "email": recep.email,
                "rol": recep.rol,
            },
        )
        return {"Authorization": f"Bearer {token}"}


# ---------------------------------------------------------------------------
# Fixtures de payloads
# ---------------------------------------------------------------------------


@pytest.fixture(scope="function")
def datos_reserva_valida():
    """Payload válido para crear una reserva."""
    return {
        "cliente_nombre": "Pedro Rojas",
        "cliente_contacto": "912345678",
        "fecha": str(date.today() + timedelta(days=2)),
        "hora": "20:00",
        "num_personas": 4,
        "tipo_ocasion": "familiar",
    }


@pytest.fixture(scope="function")
def datos_pedido_valido(platillo_visible):
    """Payload válido para crear un pedido takeaway."""
    return {
        "cliente_nombre": "María Torres",
        "cliente_contacto": "987333444",
        "items": [{"platillo_id": platillo_visible.id, "cantidad": 2}],
    }
