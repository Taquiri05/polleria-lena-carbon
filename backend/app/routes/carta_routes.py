"""Rutas del módulo CARTA — /api/categorias y /api/platillos."""
from flask import Blueprint, jsonify, request
from marshmallow import ValidationError

from app.schemas.carta_schema import (
    CategoriaCreateSchema,
    CategoriaUpdateSchema,
    PlatilloCreateSchema,
    PlatilloEstadoSchema,
    PlatilloUpdateSchema,
)
from app.services import carta_service
from app.utils.decorators import rol_requerido
from app.utils.exceptions import ServiceError

bp = Blueprint("carta", __name__)


def _manejar_error(error: ServiceError):
    respuesta = {"error": error.message}
    if error.campo:
        respuesta["campo"] = error.campo
    return jsonify(respuesta), error.status_code


# --- Categorías ---

@bp.route("/api/categorias", methods=["GET"])
def listar_categorias():
    """GET /api/categorias — Carta pública por categorías."""
    return jsonify(carta_service.listar_categorias_publicas()), 200


@bp.route("/api/categorias", methods=["POST"])
@rol_requerido("ADMIN")
def crear_categoria():
    """POST /api/categorias — Crear categoría."""
    schema = CategoriaCreateSchema()
    try:
        datos = schema.load(request.get_json() or {})
    except ValidationError as err:
        return jsonify({"error": "Datos inválidos", "detalles": err.messages}), 400

    try:
        categoria = carta_service.crear_categoria(datos)
        return jsonify(categoria), 201
    except ServiceError as e:
        return _manejar_error(e)


@bp.route("/api/categorias/<int:categoria_id>", methods=["PUT"])
@rol_requerido("ADMIN")
def actualizar_categoria(categoria_id):
    """PUT /api/categorias/:id — Editar categoría."""
    schema = CategoriaUpdateSchema()
    try:
        datos = schema.load(request.get_json() or {}, partial=True)
    except ValidationError as err:
        return jsonify({"error": "Datos inválidos", "detalles": err.messages}), 400

    try:
        categoria = carta_service.actualizar_categoria(categoria_id, datos)
        return jsonify(categoria), 200
    except ServiceError as e:
        return _manejar_error(e)


@bp.route("/api/categorias/<int:categoria_id>", methods=["DELETE"])
@rol_requerido("ADMIN")
def eliminar_categoria(categoria_id):
    """DELETE /api/categorias/:id — Eliminar categoría."""
    try:
        carta_service.eliminar_categoria(categoria_id)
        return jsonify({"message": "Categoría eliminada"}), 200
    except ServiceError as e:
        return _manejar_error(e)


# --- Platillos ---

@bp.route("/api/platillos", methods=["GET"])
def listar_platillos():
    """GET /api/platillos — Listar platillos con filtros."""
    categoria_id = request.args.get("categoria_id", type=int)
    activo_param = request.args.get("activo")

    if activo_param is not None:
        activo = activo_param.lower() in ("true", "1", "yes")
        platillos = carta_service.listar_platillos(categoria_id=categoria_id, activo=activo)
    else:
        platillos = carta_service.listar_platillos_publicos(categoria_id=categoria_id)

    return jsonify(platillos), 200


@bp.route("/api/platillos", methods=["POST"])
@rol_requerido("ADMIN")
def crear_platillo():
    """POST /api/platillos — Crear platillo."""
    schema = PlatilloCreateSchema()
    try:
        datos = schema.load(request.get_json() or {})
    except ValidationError as err:
        return jsonify({"error": "Datos inválidos", "detalles": err.messages}), 400

    try:
        platillo = carta_service.crear_platillo(datos)
        return jsonify(platillo), 201
    except ServiceError as e:
        return _manejar_error(e)


@bp.route("/api/platillos/<int:platillo_id>", methods=["PUT"])
@rol_requerido("ADMIN")
def actualizar_platillo(platillo_id):
    """PUT /api/platillos/:id — Editar platillo."""
    schema = PlatilloUpdateSchema()
    try:
        datos = schema.load(request.get_json() or {}, partial=True)
    except ValidationError as err:
        return jsonify({"error": "Datos inválidos", "detalles": err.messages}), 400

    try:
        platillo = carta_service.actualizar_platillo(platillo_id, datos)
        return jsonify(platillo), 200
    except ServiceError as e:
        return _manejar_error(e)


@bp.route("/api/platillos/<int:platillo_id>/estado", methods=["PATCH"])
@rol_requerido("ADMIN")
def cambiar_estado_platillo(platillo_id):
    """PATCH /api/platillos/:id/estado — Activar/desactivar platillo."""
    schema = PlatilloEstadoSchema()
    try:
        datos = schema.load(request.get_json() or {})
    except ValidationError as err:
        return jsonify({"error": "Datos inválidos", "detalles": err.messages}), 400

    try:
        carta_service.cambiar_visibilidad_platillo(platillo_id, datos["activo"])
        return jsonify({"message": "Visibilidad actualizada"}), 200
    except ServiceError as e:
        return _manejar_error(e)
