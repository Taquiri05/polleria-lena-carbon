"""Modelo PedidoTakeaway — pedidos para llevar."""
import secrets
import string
from datetime import datetime

from app.extensions import db


class PedidoTakeaway(db.Model):
    __tablename__ = "pedido_takeaway"

    id = db.Column(db.Integer, primary_key=True)
    cliente_nombre = db.Column(db.String(100), nullable=False)
    cliente_contacto = db.Column(db.String(20), nullable=False)
    total = db.Column(db.Numeric(10, 2), nullable=False, default=0.00)
    estado = db.Column(
        db.Enum(
            "recibido", "en_preparacion", "listo", "entregado", "cancelado",
            name="estado_pedido",
        ),
        nullable=False,
        default="recibido",
    )
    codigo_seguimiento = db.Column(db.String(20), nullable=False, unique=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    # Relación 1:N con ítems del pedido
    detalles = db.relationship(
        "DetallePedido",
        backref="pedido",
        lazy="joined",
        cascade="all, delete-orphan",
    )

    # Transiciones de estado válidas (RN-05)
    TRANSICIONES_VALIDAS = {
        "recibido": ["en_preparacion", "cancelado"],
        "en_preparacion": ["listo"],
        "listo": ["entregado"],
        "entregado": [],
        "cancelado": [],
    }

    @staticmethod
    def generar_codigo() -> str:
        """Genera un código de seguimiento único con formato TW-XXXXXXXX."""
        caracteres = string.ascii_uppercase + string.digits
        sufijo = "".join(secrets.choice(caracteres) for _ in range(8))
        return f"TW-{sufijo}"

    def puede_transicionar(self, nuevo_estado: str) -> bool:
        """Valida si la transición de estado es permitida (RN-05)."""
        return nuevo_estado in self.TRANSICIONES_VALIDAS.get(self.estado, [])

    def to_dict(self, include_detalles: bool = True) -> dict:
        data = {
            "id": self.id,
            "cliente_nombre": self.cliente_nombre,
            "cliente_contacto": self.cliente_contacto,
            "total": float(self.total),
            "estado": self.estado,
            "codigo_seguimiento": self.codigo_seguimiento,
            "created_at": self.created_at.isoformat(),
        }
        if include_detalles:
            data["items"] = [d.to_dict() for d in self.detalles]
        return data

    def __repr__(self) -> str:
        return f"<PedidoTakeaway {self.codigo_seguimiento} [{self.estado}]>"
