"""Rutas del módulo RESERVAS — /api/reservas."""
from datetime import date

from flask import Blueprint, jsonify, request
from marshmallow import ValidationError

from app.schemas.reserva_schema import (
    ReservaCancelarSchema,
    ReservaCreateSchema,
    ReservaDisponibilidadSchema,
    ReservaEstadoSchema,
)
from app.services import reserva_service
from app.utils.decorators import staff_requerido
from app.utils.exceptions import ServiceError

bp = Blueprint("reservas", __name__, url_prefix="/api/reservas")


def _manejar_error(error: ServiceError):
    respuesta = {"error": error.message}
    if error.campo:
        respuesta["campo"] = error.campo
    return jsonify(respuesta), error.status_code


@bp.route("/disponibilidad", methods=["GET"])
def disponibilidad():
    """GET /api/reservas/disponibilidad — Consultar disponibilidad."""
    schema = ReservaDisponibilidadSchema()
    params = {
        "fecha": request.args.get("fecha"),
        "hora": request.args.get("hora") or None,
        "tipo_ocasion": request.args.get("tipo_ocasion"),
        "num_personas": request.args.get("num_personas", type=int),
    }
    try:
        datos = schema.load(params)
    except ValidationError as err:
        return jsonify({"error": "Datos inválidos", "detalles": err.messages}), 400

    try:
        resultado = reserva_service.consultar_disponibilidad(
            datos["fecha"],
            datos["tipo_ocasion"],
            datos["num_personas"],
            datos.get("hora"),
        )
        return jsonify(resultado), 200
    except ServiceError as e:
        return _manejar_error(e)


@bp.route("", methods=["POST"])
def crear():
    """POST /api/reservas — Crear reserva con asignación automática."""
    schema = ReservaCreateSchema()
    try:
        datos = schema.load(request.get_json() or {})
    except ValidationError as err:
        return jsonify({"error": "Datos inválidos", "detalles": err.messages}), 400

    try:
        reserva = reserva_service.crear_reserva(datos)
        return jsonify(reserva), 201
    except ServiceError as e:
        return _manejar_error(e)


@bp.route("", methods=["GET"])
@staff_requerido
def listar():
    """GET /api/reservas — Listar reservas con filtros."""
    fecha_str = request.args.get("fecha")
    estado = request.args.get("estado")

    fecha = date.fromisoformat(fecha_str) if fecha_str else None
    reservas = reserva_service.listar_reservas(fecha=fecha, estado=estado)
    return jsonify(reservas), 200


@bp.route("/<int:reserva_id>", methods=["GET"])
@staff_requerido
def obtener(reserva_id):
    """GET /api/reservas/:id — Detalle de reserva."""
    try:
        reserva = reserva_service.obtener_reserva(reserva_id)
        return jsonify(reserva), 200
    except ServiceError as e:
        return _manejar_error(e)


@bp.route("/<int:reserva_id>/estado", methods=["PATCH"])
@staff_requerido
def actualizar_estado(reserva_id):
    """PATCH /api/reservas/:id/estado — Actualizar estado."""
    schema = ReservaEstadoSchema()
    try:
        datos = schema.load(request.get_json() or {})
    except ValidationError as err:
        return jsonify({"error": "Datos inválidos", "detalles": err.messages}), 400

    try:
        resultado = reserva_service.actualizar_estado_reserva(reserva_id, datos["estado"])
        return jsonify(resultado), 200
    except ServiceError as e:
        return _manejar_error(e)


@bp.route("/cancelar", methods=["POST"])
def cancelar():
    """POST /api/reservas/cancelar — Cancelar reserva por código."""
    schema = ReservaCancelarSchema()
    try:
        datos = schema.load(request.get_json() or {})
    except ValidationError as err:
        return jsonify({"error": "Datos inválidos", "detalles": err.messages}), 400

    try:
        reserva_service.cancelar_reserva_por_codigo(datos["codigo_confirmacion"])
        return jsonify({"message": "Reserva cancelada correctamente"}), 200
    except ServiceError as e:
        return _manejar_error(e)
