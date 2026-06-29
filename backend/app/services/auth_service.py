"""Servicios del módulo de autenticación y gestión de usuarios."""
from datetime import timedelta
from typing import Optional

from flask_jwt_extended import create_access_token

from app.extensions import agregar_token_blocklist, db
from app.models.configuracion import Configuracion
from app.models.usuario import Usuario
from app.utils.exceptions import ServiceError


def _obtener_expiracion_jwt() -> timedelta:
    """Lee las horas de expiración JWT desde la tabla Configuracion (RN-10)."""
    horas = Configuracion.get_valor("jwt_expiration_hours", "8")
    try:
        return timedelta(hours=int(horas))
    except (TypeError, ValueError):
        return timedelta(hours=8)


def autenticar_usuario(email: str, password: str) -> dict:
    """
    Valida credenciales y retorna token JWT con datos del usuario.
    CU-02: Iniciar Sesión.
    """
    usuario = Usuario.query.filter_by(email=email).first()

    if not usuario or not usuario.check_password(password):
        raise ServiceError("Credenciales inválidas.", 401)

    if not usuario.activo:
        raise ServiceError("Cuenta desactivada. Contacte al administrador.", 403)

    expiracion = _obtener_expiracion_jwt()
    token = create_access_token(
        identity=str(usuario.id),
        additional_claims={
            "user_id": usuario.id,
            "email": usuario.email,
            "rol": usuario.rol,
        },
        expires_delta=expiracion,
    )

    return {
        "access_token": token,
        "usuario": {
            "id": usuario.id,
            "nombre": usuario.nombre,
            "email": usuario.email,
            "rol": usuario.rol,
        },
    }


def cerrar_sesion(jti: str) -> None:
    """Invalida el token JWT activo agregándolo a la blocklist (RF-26)."""
    agregar_token_blocklist(jti)


def obtener_usuario_por_id(usuario_id: int) -> Usuario:
    """Obtiene un usuario por ID o lanza 404."""
    usuario = db.session.get(Usuario, usuario_id)
    if not usuario:
        raise ServiceError("Usuario no encontrado.", 404)
    return usuario


def obtener_perfil(usuario_id: int) -> dict:
    """Retorna los datos del perfil del usuario autenticado."""
    usuario = obtener_usuario_por_id(usuario_id)
    return {
        "id": usuario.id,
        "nombre": usuario.nombre,
        "email": usuario.email,
        "rol": usuario.rol,
    }


def cambiar_password(usuario_id: int, password_actual: str, password_nueva: str) -> None:
    """Cambia la contraseña del usuario autenticado (RF-28)."""
    usuario = obtener_usuario_por_id(usuario_id)

    if not usuario.check_password(password_actual):
        raise ServiceError("Contraseña actual incorrecta.", 400, campo="password_actual")

    usuario.set_password(password_nueva)
    db.session.commit()


def listar_usuarios() -> list[dict]:
    """Lista todos los usuarios del sistema (RF-27)."""
    return [u.to_dict(include_created_at=False) for u in Usuario.query.order_by(Usuario.id).all()]


def crear_usuario(datos: dict) -> dict:
    """Crea un nuevo usuario staff (RF-27)."""
    if Usuario.query.filter_by(email=datos["email"]).first():
        raise ServiceError("El correo electrónico ya está registrado.", 409, campo="email")

    usuario = Usuario(
        nombre=datos["nombre"],
        email=datos["email"],
        rol=datos["rol"],
        activo=True,
    )
    usuario.set_password(datos["password"])
    db.session.add(usuario)
    db.session.commit()
    return usuario.to_dict(include_created_at=False)


def actualizar_usuario(usuario_id: int, datos: dict) -> dict:
    """Actualiza datos de un usuario existente."""
    usuario = obtener_usuario_por_id(usuario_id)

    if "email" in datos and datos["email"] != usuario.email:
        if Usuario.query.filter_by(email=datos["email"]).first():
            raise ServiceError("El correo electrónico ya está registrado.", 409, campo="email")
        usuario.email = datos["email"]

    if "nombre" in datos:
        usuario.nombre = datos["nombre"]
    if "rol" in datos:
        usuario.rol = datos["rol"]

    db.session.commit()
    return usuario.to_dict(include_created_at=False)


def cambiar_estado_usuario(usuario_id: int, activo: bool) -> None:
    """Activa o desactiva una cuenta de usuario."""
    usuario = obtener_usuario_por_id(usuario_id)
    usuario.activo = activo
    db.session.commit()
