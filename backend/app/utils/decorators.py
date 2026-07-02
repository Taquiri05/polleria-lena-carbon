"""Decoradores de autorización por rol."""
from functools import wraps

from flask import jsonify
from flask_jwt_extended import get_jwt, jwt_required


def rol_requerido(*roles):
    """
    Decorador que exige JWT válido y uno de los roles indicados.
    Retorna 403 si el rol del usuario no está autorizado.
    """

    def decorator(fn):
        @wraps(fn)
        @jwt_required()
        def wrapper(*args, **kwargs):
            claims = get_jwt()
            if claims.get("rol") not in roles:
                return jsonify({"error": "Acceso denegado"}), 403
            return fn(*args, **kwargs)

        return wrapper

    return decorator


def staff_requerido(fn):
    """Decorador: requiere rol RECEPCIONISTA o ADMIN."""

    @wraps(fn)
    @jwt_required()
    def wrapper(*args, **kwargs):
        claims = get_jwt()
        if claims.get("rol") not in ("ADMIN", "RECEPCIONISTA"):
            return jsonify({"error": "Acceso denegado"}), 403
        return fn(*args, **kwargs)

    return wrapper
