"""Excepciones de dominio del backend."""
from typing import Optional


class ServiceError(Exception):
    """Excepción base para errores de la capa de servicios."""

    def __init__(self, message: str, status_code: int = 400, campo: Optional[str] = None):
        self.message = message
        self.status_code = status_code
        self.campo = campo
        super().__init__(message)
