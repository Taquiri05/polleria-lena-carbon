"""Modelo Categoria — categorías del menú digital."""
from app.extensions import db


class Categoria(db.Model):
    __tablename__ = "categoria"

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False, unique=True)
    descripcion = db.Column(db.Text)
    activo = db.Column(db.Boolean, nullable=False, default=True)

    # Relación inversa
    platillos = db.relationship("Platillo", backref="categoria", lazy="dynamic")

    def to_dict(self, include_platillos: bool = False, solo_activos: bool = True) -> dict:
        data = {
            "id": self.id,
            "nombre": self.nombre,
            "descripcion": self.descripcion,
            "activo": self.activo,
        }
        if include_platillos:
            query = self.platillos
            if solo_activos:
                query = query.filter_by(activo=True)
            data["platillos"] = [
                {
                    "id": p.id,
                    "nombre": p.nombre,
                    "precio": float(p.precio),
                    "imagen_url": p.imagen_url,
                }
                for p in query.all()
            ]
        return data

    def __repr__(self) -> str:
        return f"<Categoria {self.nombre}>"
