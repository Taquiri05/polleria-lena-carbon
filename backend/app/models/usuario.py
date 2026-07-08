"""Modelo Usuario — staff del restaurante (Admin y Recepcionista)."""
import bcrypt
from datetime import datetime

from app.extensions import db


class Usuario(db.Model):
    __tablename__ = "usuario"

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), nullable=False, unique=True)
    password_hash = db.Column(db.String(255), nullable=False)
    rol = db.Column(
        db.Enum("ADMIN", "RECEPCIONISTA", name="rol_usuario"),
        nullable=False,
        default="RECEPCIONISTA",
    )
    activo = db.Column(db.Boolean, nullable=False, default=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)

    def set_password(self, password: str) -> None:
        """Hashea la contraseña con bcrypt (12 rounds) y la almacena."""
        self.password_hash = bcrypt.hashpw(
            password.encode("utf-8"),
            bcrypt.gensalt(rounds=12),
        ).decode("utf-8")

    def check_password(self, password: str) -> bool:
        """Verifica la contraseña contra el hash almacenado."""
        return bcrypt.checkpw(
            password.encode("utf-8"),
            self.password_hash.encode("utf-8"),
        )

    def to_dict(self, include_created_at: bool = True) -> dict:
        data = {
            "id": self.id,
            "nombre": self.nombre,
            "email": self.email,
            "rol": self.rol,
            "activo": self.activo,
        }
        if include_created_at:
            data["created_at"] = self.created_at.isoformat()
        return data

    def __repr__(self) -> str:
        return f"<Usuario {self.email} [{self.rol}]>"
