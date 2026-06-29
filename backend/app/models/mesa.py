"""Modelo Mesa — mesas físicas del restaurante."""
from app.extensions import db


class Mesa(db.Model):
    __tablename__ = "mesa"

    id = db.Column(db.Integer, primary_key=True)
    numero = db.Column(db.Integer, nullable=False, unique=True)
    capacidad = db.Column(db.SmallInteger, nullable=False)
    tipo_ocasion = db.Column(
        db.Enum("familiar", "romantica", "reunion", name="tipo_ocasion_mesa"),
        nullable=False,
    )
    activo = db.Column(db.Boolean, nullable=False, default=True)

    # Relación inversa: una mesa puede tener muchas reservas
    reservas = db.relationship("Reserva", backref="mesa", lazy="dynamic")

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "numero": self.numero,
            "capacidad": self.capacidad,
            "tipo_ocasion": self.tipo_ocasion,
            "activo": self.activo,
        }

    def __repr__(self) -> str:
        return f"<Mesa #{self.numero} [{self.tipo_ocasion}] cap={self.capacidad}>"
