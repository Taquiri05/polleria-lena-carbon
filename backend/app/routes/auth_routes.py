"""Rutas del módulo AUTH — /api/auth."""

from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt, get_jwt_identity, jwt_required
from marshmallow import ValidationError

from app.schemas.usuario_schema import CambiarPasswordSchema, LoginSchema
from app.services import auth_service
from app.utils.exceptions import ServiceError

bp = Blueprint("auth", __name__, url_prefix="/api/auth")


def _manejar_error_servicio(error: ServiceError):
    respuesta = {"error": error.message}
    if error.campo:
        respuesta["campo"] = error.campo
    return jsonify(respuesta), error.status_code


@bp.route("/login", methods=["POST"])
def login():
    """POST /api/auth/login — Autenticación con credenciales."""
    schema = LoginSchema()
    try:
        datos = schema.load(request.get_json() or {})
    except ValidationError as err:
        return jsonify({"error": "Datos inválidos", "detalles": err.messages}), 400

    try:
        resultado = auth_service.autenticar_usuario(datos["email"], datos["password"])
        return jsonify(resultado), 200
    except ServiceError as e:
        return _manejar_error_servicio(e)


@bp.route("/logout", methods=["POST"])
@jwt_required()
def logout():
    """POST /api/auth/logout — Invalidación del token activo."""
    jti = get_jwt()["jti"]
    auth_service.cerrar_sesion(jti)
    return jsonify({"message": "Sesión cerrada correctamente"}), 200


@bp.route("/cambiar-password", methods=["PUT"])
@jwt_required()
def cambiar_password():
    """PUT /api/auth/cambiar-password — Cambio de contraseña."""
    schema = CambiarPasswordSchema()
    body = request.get_json() or {}
    try:
        datos = schema.load(body)
    except ValidationError as err:
        return jsonify({"error": "Datos inválidos", "detalles": err.messages}), 400

    try:
        auth_service.cambiar_password(
            int(get_jwt_identity()),
            datos["password_actual"],
            datos["password_nueva"],
        )
        return jsonify({"message": "Contraseña actualizada"}), 200
    except ServiceError as e:
        return _manejar_error_servicio(e)


@bp.route("/perfil", methods=["GET"])
@jwt_required()
def perfil():
    """GET /api/auth/perfil — Datos del usuario autenticado."""
    try:
        perfil_data = auth_service.obtener_perfil(int(get_jwt_identity()))
        return jsonify(perfil_data), 200
    except ServiceError as e:
        return _manejar_error_servicio(e)
