"""Modelo Configuracion — parámetros configurables del sistema."""
from app.extensions import db


class Configuracion(db.Model):
    __tablename__ = "configuracion"

    id = db.Column(db.Integer, primary_key=True)
    clave = db.Column(db.String(100), nullable=False, unique=True)
    valor = db.Column(db.String(500), nullable=False)

    # Claves permitidas (validación en capa de servicios)
    CLAVES_PERMITIDAS = {
        "nombre_negocio",
        "horario_apertura",
        "horario_cierre",
        "contacto_telefono",
        "contacto_email",
        "jwt_expiration_hours",
        "max_personas_reserva",
        "bloqueo_reserva_horas",
        "cancelacion_min_horas",
        "moneda",
    }

    @classmethod
    def get_valor(cls, clave: str, default=None):
        """Obtiene el valor de una clave de configuración."""
        config = cls.query.filter_by(clave=clave).first()
        return config.valor if config else default

    @classmethod
    def get_all_dict(cls) -> dict:
        """Retorna toda la configuración como diccionario clave:valor."""
        return {c.clave: c.valor for c in cls.query.all()}

    def to_dict(self) -> dict:
        return {"clave": self.clave, "valor": self.valor}

    def __repr__(self) -> str:
        return f"<Configuracion {self.clave}={self.valor}>"
