"""Rutas del módulo TAKEAWAY — /api/takeaway."""
from datetime import date

from flask import Blueprint, jsonify, request
from marshmallow import ValidationError

from app.schemas.takeaway_schema import TakeawayCreateSchema, TakeawayEstadoSchema
from app.services import takeaway_service
from app.utils.decorators import staff_requerido
from app.utils.exceptions import ServiceError

bp = Blueprint("takeaway", __name__, url_prefix="/api/takeaway")


def _manejar_error(error: ServiceError):
    respuesta = {"error": error.message}
    if error.campo:
        respuesta["campo"] = error.campo
    return jsonify(respuesta), error.status_code


@bp.route("", methods=["POST"])
def crear():
    """POST /api/takeaway — Crear pedido takeaway."""
    schema = TakeawayCreateSchema()
    try:
        datos = schema.load(request.get_json() or {})
    except ValidationError as err:
        return jsonify({"error": "Datos inválidos", "detalles": err.messages}), 400

    try:
        pedido = takeaway_service.crear_pedido_takeaway(datos)
        return jsonify(pedido), 201
    except ServiceError as e:
        return _manejar_error(e)


@bp.route("/estado/<codigo>", methods=["GET"])
def consultar_estado(codigo):
    """GET /api/takeaway/estado/:codigo — Consultar estado por código."""
    try:
        pedido = takeaway_service.consultar_estado_por_codigo(codigo)
        return jsonify(pedido), 200
    except ServiceError as e:
        return _manejar_error(e)


@bp.route("", methods=["GET"])
@staff_requerido
def listar():
    """GET /api/takeaway — Listar pedidos con filtros."""
    fecha_str = request.args.get("fecha")
    estado = request.args.get("estado")
    fecha = date.fromisoformat(fecha_str) if fecha_str else None

    pedidos = takeaway_service.listar_pedidos(fecha=fecha, estado=estado)
    return jsonify(pedidos), 200


@bp.route("/<int:pedido_id>", methods=["GET"])
@staff_requerido
def obtener(pedido_id):
    """GET /api/takeaway/:id — Detalle de pedido."""
    try:
        pedido = takeaway_service.obtener_pedido(pedido_id)
        return jsonify(pedido), 200
    except ServiceError as e:
        return _manejar_error(e)


@bp.route("/<int:pedido_id>/estado", methods=["PATCH"])
@staff_requerido
def actualizar_estado(pedido_id):
    """PATCH /api/takeaway/:id/estado — Actualizar estado del pedido."""
    schema = TakeawayEstadoSchema()
    try:
        datos = schema.load(request.get_json() or {})
    except ValidationError as err:
        return jsonify({"error": "Datos inválidos", "detalles": err.messages}), 400

    try:
        resultado = takeaway_service.actualizar_estado_pedido(pedido_id, datos["estado"])
        return jsonify(resultado), 200
    except ServiceError as e:
        return _manejar_error(e)
