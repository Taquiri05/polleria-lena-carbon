"""Servicios del módulo de mesas."""
from app.extensions import db
from app.models.mesa import Mesa
from app.utils.exceptions import ServiceError


def listar_mesas(solo_activas: bool = True) -> list[dict]:
    """Lista mesas del restaurante."""
    query = Mesa.query
    if solo_activas:
        query = query.filter_by(activo=True)
    return [m.to_dict() for m in query.order_by(Mesa.numero).all()]


def obtener_mesa(mesa_id: int) -> Mesa:
    """Obtiene una mesa por ID."""
    mesa = db.session.get(Mesa, mesa_id)
    if not mesa:
        raise ServiceError("Mesa no encontrada.", 404)
    return mesa


def crear_mesa(datos: dict) -> dict:
    """Registra una nueva mesa (RF-08)."""
    if Mesa.query.filter_by(numero=datos["numero"]).first():
        raise ServiceError("Número de mesa duplicado.", 409, campo="numero")

    mesa = Mesa(
        numero=datos["numero"],
        capacidad=datos["capacidad"],
        tipo_ocasion=datos["tipo_ocasion"],
        activo=True,
    )
    db.session.add(mesa)
    db.session.commit()
    return mesa.to_dict()


def actualizar_mesa(mesa_id: int, datos: dict) -> dict:
    """Edita datos de una mesa existente."""
    mesa = obtener_mesa(mesa_id)

    if "numero" in datos and datos["numero"] != mesa.numero:
        if Mesa.query.filter_by(numero=datos["numero"]).first():
            raise ServiceError("Número de mesa duplicado.", 409, campo="numero")
        mesa.numero = datos["numero"]

    if "capacidad" in datos:
        mesa.capacidad = datos["capacidad"]
    if "tipo_ocasion" in datos:
        mesa.tipo_ocasion = datos["tipo_ocasion"]

    db.session.commit()
    return mesa.to_dict()


def cambiar_estado_mesa(mesa_id: int, activo: bool) -> None:
    """Activa o desactiva una mesa."""
    mesa = obtener_mesa(mesa_id)
    mesa.activo = activo
    db.session.commit()
