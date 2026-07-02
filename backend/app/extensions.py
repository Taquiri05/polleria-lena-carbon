"""Instancias globales de extensiones Flask (patrón Application Factory)."""
from flask_jwt_extended import JWTManager
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
jwt = JWTManager()
ma = Marshmallow()

# Blocklist en memoria para tokens invalidados al cerrar sesión
_jwt_blocklist: set[str] = set()


def agregar_token_blocklist(jti: str) -> None:
    """Agrega un JTI a la blocklist de tokens invalidados."""
    _jwt_blocklist.add(jti)


def es_token_blocklist(jti: str) -> bool:
    """Verifica si un JTI está en la blocklist."""
    return jti in _jwt_blocklist
