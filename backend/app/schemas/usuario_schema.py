"""Schemas Marshmallow para el módulo de usuarios y autenticación."""
from marshmallow import Schema, fields, validate, validates, ValidationError


class UsuarioSchema(Schema):
    """Schema de serialización de usuario (sin contraseña)."""

    id = fields.Int(dump_only=True)
    nombre = fields.Str(required=True)
    email = fields.Email(required=True)
    rol = fields.Str(validate=validate.OneOf(["ADMIN", "RECEPCIONISTA"]))
    activo = fields.Bool()
    created_at = fields.DateTime(dump_only=True)


class UsuarioCreateSchema(Schema):
    """Schema para creación de usuario por administrador."""

    nombre = fields.Str(required=True, validate=validate.Length(min=2, max=100))
    email = fields.Email(required=True)
    password = fields.Str(required=True, validate=validate.Length(min=8, max=128))
    rol = fields.Str(
        required=True,
        validate=validate.OneOf(["ADMIN", "RECEPCIONISTA"]),
    )


class UsuarioUpdateSchema(Schema):
    """Schema para actualización parcial de usuario."""

    nombre = fields.Str(validate=validate.Length(min=2, max=100))
    email = fields.Email()
    rol = fields.Str(validate=validate.OneOf(["ADMIN", "RECEPCIONISTA"]))


class LoginSchema(Schema):
    """Schema para inicio de sesión."""

    email = fields.Email(required=True)
    password = fields.Str(required=True)


class CambiarPasswordSchema(Schema):
    """Schema para cambio de contraseña del usuario autenticado."""

    password_actual = fields.Str(required=True)
    password_nueva = fields.Str(required=True, validate=validate.Length(min=8, max=128))

    @validates("password_nueva")
    def validar_password_nueva(self, value):
        if value == self.context.get("password_actual"):
            raise ValidationError("La nueva contraseña debe ser diferente a la actual.")
