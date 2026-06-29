"""Rutas del módulo MESAS — /api/mesas."""
from flask import Blueprint, jsonify, request
from marshmallow import ValidationError

from app.schemas.mesa_schema import MesaCreateSchema, MesaEstadoSchema, MesaUpdateSchema
from app.services import mesa_service
from app.utils.decorators import rol_requerido, staff_requerido
from app.utils.exceptions import ServiceError

bp = Blueprint("mesas", __name__, url_prefix="/api/mesas")


def _manejar_error(error: ServiceError):
    respuesta = {"error": error.message}
    if error.campo:
        respuesta["campo"] = error.campo
    return jsonify(respuesta), error.status_code


@bp.route("", methods=["GET"])
@staff_requerido
def listar():
    """GET /api/mesas — Listar mesas activas."""
    return jsonify(mesa_service.listar_mesas(solo_activas=True)), 200


@bp.route("", methods=["POST"])
@rol_requerido("ADMIN")
def crear():
    """POST /api/mesas — Registrar nueva mesa."""
    schema = MesaCreateSchema()
    try:
        datos = schema.load(request.get_json() or {})
    except ValidationError as err:
        return jsonify({"error": "Datos inválidos", "detalles": err.messages}), 400

    try:
        mesa = mesa_service.crear_mesa(datos)
        return jsonify(mesa), 201
    except ServiceError as e:
        return _manejar_error(e)


@bp.route("/<int:mesa_id>", methods=["PUT"])
@rol_requerido("ADMIN")
def actualizar(mesa_id):
    """PUT /api/mesas/:id — Editar mesa."""
    schema = MesaUpdateSchema()
    try:
        datos = schema.load(request.get_json() or {}, partial=True)
    except ValidationError as err:
        return jsonify({"error": "Datos inválidos", "detalles": err.messages}), 400

    try:
        mesa = mesa_service.actualizar_mesa(mesa_id, datos)
        return jsonify(mesa), 200
    except ServiceError as e:
        return _manejar_error(e)


@bp.route("/<int:mesa_id>/estado", methods=["PATCH"])
@rol_requerido("ADMIN")
def cambiar_estado(mesa_id):
    """PATCH /api/mesas/:id/estado — Activar/desactivar mesa."""
    schema = MesaEstadoSchema()
    try:
        datos = schema.load(request.get_json() or {})
    except ValidationError as err:
        return jsonify({"error": "Datos inválidos", "detalles": err.messages}), 400

    try:
        mesa_service.cambiar_estado_mesa(mesa_id, datos["activo"])
        return jsonify({"message": "Estado actualizado"}), 200
    except ServiceError as e:
        return _manejar_error(e)
