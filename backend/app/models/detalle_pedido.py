"""Modelo DetallePedido — ítems individuales de un pedido takeaway."""
from app.extensions import db


class DetallePedido(db.Model):
    __tablename__ = "detalle_pedido"

    id = db.Column(db.Integer, primary_key=True)
    pedido_id = db.Column(
        db.Integer,
        db.ForeignKey("pedido_takeaway.id", ondelete="CASCADE"),
        nullable=False,
    )
    platillo_id = db.Column(
        db.Integer,
        db.ForeignKey("platillo.id", ondelete="RESTRICT"),
        nullable=False,
    )
    cantidad = db.Column(db.SmallInteger, nullable=False)
    precio_unitario = db.Column(db.Numeric(8, 2), nullable=False)

    @property
    def subtotal(self) -> float:
        """Calcula el subtotal del ítem (cantidad × precio unitario)."""
        return float(self.cantidad) * float(self.precio_unitario)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "platillo_id": self.platillo_id,
            "platillo": self.platillo.nombre if self.platillo else None,
            "platillo_nombre": self.platillo.nombre if self.platillo else None,
            "cantidad": self.cantidad,
            "precio_unitario": float(self.precio_unitario),
            "subtotal": self.subtotal,
        }

    def __repr__(self) -> str:
        return f"<DetallePedido pedido={self.pedido_id} platillo={self.platillo_id} x{self.cantidad}>"
