"""Modelo Reserva — reservas de mesas realizadas por clientes."""
import secrets
import string
from datetime import datetime

from app.extensions import db


class Reserva(db.Model):
    __tablename__ = "reserva"

    id = db.Column(db.Integer, primary_key=True)
    cliente_nombre = db.Column(db.String(100), nullable=False)
    cliente_contacto = db.Column(db.String(20), nullable=False)
    fecha = db.Column(db.Date, nullable=False)
    hora = db.Column(db.Time, nullable=False)
    num_personas = db.Column(db.SmallInteger, nullable=False)
    tipo_ocasion = db.Column(
        db.Enum("familiar", "romantica", "reunion", name="tipo_ocasion_reserva"),
        nullable=False,
    )
    estado = db.Column(
        db.Enum(
            "pendiente", "confirmada", "completada", "cancelada",
            name="estado_reserva",
        ),
        nullable=False,
        default="pendiente",
    )
    codigo_confirmacion = db.Column(db.String(20), nullable=False, unique=True)
    mesa_id = db.Column(
        db.Integer,
        db.ForeignKey("mesa.id", ondelete="RESTRICT"),
        nullable=False,
    )
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)

    # Transiciones de estado válidas
    TRANSICIONES_VALIDAS = {
        "pendiente": ["confirmada", "cancelada"],
        "confirmada": ["completada", "cancelada"],
        "completada": [],
        "cancelada": [],
    }

    @staticmethod
    def generar_codigo() -> str:
        """Genera un código de confirmación único con formato POLL-XXXXXX."""
        caracteres = string.ascii_uppercase + string.digits
        sufijo = "".join(secrets.choice(caracteres) for _ in range(6))
        return f"POLL-{sufijo}"

    def puede_transicionar(self, nuevo_estado: str) -> bool:
        """Valida si la transición de estado es permitida."""
        return nuevo_estado in self.TRANSICIONES_VALIDAS.get(self.estado, [])

    def to_dict(self, include_mesa: bool = False) -> dict:
        data = {
            "id": self.id,
            "cliente_nombre": self.cliente_nombre,
            "cliente_contacto": self.cliente_contacto,
            "fecha": self.fecha.isoformat(),
            "hora": str(self.hora),
            "num_personas": self.num_personas,
            "tipo_ocasion": self.tipo_ocasion,
            "estado": self.estado,
            "codigo_confirmacion": self.codigo_confirmacion,
            "mesa_id": self.mesa_id,
            "created_at": self.created_at.isoformat(),
        }
        if include_mesa and self.mesa:
            data["mesa"] = {"numero": self.mesa.numero, "capacidad": self.mesa.capacidad}
        return data

    def __repr__(self) -> str:
        return f"<Reserva {self.codigo_confirmacion} [{self.estado}]>"
