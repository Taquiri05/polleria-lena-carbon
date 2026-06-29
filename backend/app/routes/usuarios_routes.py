"""Rutas del módulo USUARIOS — /api/usuarios."""
from flask import Blueprint, jsonify, request
from marshmallow import ValidationError

from app.schemas.usuario_schema import UsuarioCreateSchema, UsuarioUpdateSchema
from app.services import auth_service
from app.utils.decorators import rol_requerido
from app.utils.exceptions import ServiceError

bp = Blueprint("usuarios", __name__, url_prefix="/api/usuarios")


def _manejar_error(error: ServiceError):
    respuesta = {"error": error.message}
    if error.campo:
        respuesta["campo"] = error.campo
    return jsonify(respuesta), error.status_code


@bp.route("", methods=["GET"])
@rol_requerido("ADMIN")
def listar():
    """GET /api/usuarios — Listar todos los usuarios."""
    return jsonify(auth_service.listar_usuarios()), 200


@bp.route("", methods=["POST"])
@rol_requerido("ADMIN")
def crear():
    """POST /api/usuarios — Crear nuevo usuario."""
    schema = UsuarioCreateSchema()
    try:
        datos = schema.load(request.get_json() or {})
    except ValidationError as err:
        return jsonify({"error": "Datos inválidos", "detalles": err.messages}), 400

    try:
        usuario = auth_service.crear_usuario(datos)
        return jsonify(usuario), 201
    except ServiceError as e:
        return _manejar_error(e)


@bp.route("/<int:usuario_id>", methods=["GET"])
@rol_requerido("ADMIN")
def obtener(usuario_id):
    """GET /api/usuarios/:id — Detalle de usuario."""
    try:
        usuario = auth_service.obtener_usuario_por_id(usuario_id)
        return jsonify(usuario.to_dict()), 200
    except ServiceError as e:
        return _manejar_error(e)


@bp.route("/<int:usuario_id>", methods=["PUT"])
@rol_requerido("ADMIN")
def actualizar(usuario_id):
    """PUT /api/usuarios/:id — Editar usuario."""
    schema = UsuarioUpdateSchema()
    try:
        datos = schema.load(request.get_json() or {}, partial=True)
    except ValidationError as err:
        return jsonify({"error": "Datos inválidos", "detalles": err.messages}), 400

    if not datos:
        return jsonify({"error": "No se enviaron datos para actualizar."}), 400

    try:
        usuario = auth_service.actualizar_usuario(usuario_id, datos)
        return jsonify(usuario), 200
    except ServiceError as e:
        return _manejar_error(e)


@bp.route("/<int:usuario_id>/estado", methods=["PATCH"])
@rol_requerido("ADMIN")
def cambiar_estado(usuario_id):
    """PATCH /api/usuarios/:id/estado — Activar/desactivar usuario."""
    body = request.get_json() or {}
    if "activo" not in body:
        return jsonify({"error": "El campo 'activo' es obligatorio."}), 400

    try:
        auth_service.cambiar_estado_usuario(usuario_id, bool(body["activo"]))
        return jsonify({"message": "Estado actualizado"}), 200
    except ServiceError as e:
        return _manejar_error(e)
