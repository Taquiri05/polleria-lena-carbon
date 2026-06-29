"""Modelo Platillo — platillos del menú digital."""
from app.extensions import db


class Platillo(db.Model):
    __tablename__ = "platillo"

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(150), nullable=False)
    descripcion = db.Column(db.Text)
    precio = db.Column(db.Numeric(8, 2), nullable=False)
    imagen_url = db.Column(db.String(500))
    activo = db.Column(db.Boolean, nullable=False, default=True)
    categoria_id = db.Column(
        db.Integer,
        db.ForeignKey("categoria.id", ondelete="RESTRICT"),
        nullable=False,
    )

    # Relación inversa
    detalles = db.relationship("DetallePedido", backref="platillo", lazy="dynamic")

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "nombre": self.nombre,
            "descripcion": self.descripcion,
            "precio": float(self.precio),
            "imagen_url": self.imagen_url,
            "activo": self.activo,
            "categoria_id": self.categoria_id,
            "categoria": self.categoria.nombre if self.categoria else None,
        }

    def __repr__(self) -> str:
        return f"<Platillo {self.nombre} S/{self.precio}>"
