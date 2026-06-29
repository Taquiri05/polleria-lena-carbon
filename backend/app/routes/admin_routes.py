"""Rutas del módulo ADMIN — /api/admin."""
from datetime import date

from flask import Blueprint, jsonify, request

from app.services import admin_service, reserva_service, takeaway_service
from app.utils.decorators import rol_requerido
from app.utils.exceptions import ServiceError

bp = Blueprint("admin", __name__, url_prefix="/api/admin")


def _manejar_error(error: ServiceError):
    return jsonify({"error": error.message}), error.status_code


@bp.route("/dashboard", methods=["GET"])
@rol_requerido("ADMIN")
def dashboard():
    """GET /api/admin/dashboard — Métricas del día."""
    return jsonify(admin_service.obtener_dashboard()), 200


@bp.route("/configuracion", methods=["GET"])
@rol_requerido("ADMIN")
def obtener_configuracion():
    """GET /api/admin/configuracion — Configuración del sistema."""
    return jsonify(admin_service.obtener_configuracion()), 200


@bp.route("/configuracion", methods=["PUT"])
@rol_requerido("ADMIN")
def actualizar_configuracion():
    """PUT /api/admin/configuracion — Actualizar configuración."""
    body = request.get_json()
    if not body:
        return jsonify({"error": "Se requiere un cuerpo JSON válido."}), 400

    try:
        admin_service.actualizar_configuracion(body)
        return jsonify({"message": "Configuración actualizada"}), 200
    except ServiceError as e:
        return _manejar_error(e)


@bp.route("/reservas/historial", methods=["GET"])
@rol_requerido("ADMIN")
def historial_reservas():
    """GET /api/admin/reservas/historial — Historial de reservas (RF-23)."""
    fecha_str = request.args.get("fecha")
    estado = request.args.get("estado")
    fecha = date.fromisoformat(fecha_str) if fecha_str else None

    reservas = reserva_service.listar_reservas(fecha=fecha, estado=estado)
    return jsonify(reservas), 200


@bp.route("/takeaway/historial", methods=["GET"])
@rol_requerido("ADMIN")
def historial_pedidos():
    """GET /api/admin/takeaway/historial — Historial de pedidos (RF-24)."""
    fecha_str = request.args.get("fecha")
    estado = request.args.get("estado")
    fecha = date.fromisoformat(fecha_str) if fecha_str else None

    pedidos = takeaway_service.listar_pedidos(fecha=fecha, estado=estado)
    return jsonify(pedidos), 200
