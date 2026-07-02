"""Schemas Marshmallow para el módulo de reservas."""
from marshmallow import Schema, fields, validate


TIPOS_OCASION = ("familiar", "romantica", "reunion")
ESTADOS_RESERVA = ("pendiente", "confirmada", "completada", "cancelada")


class ReservaCreateSchema(Schema):
    """Schema para creación de reserva por cliente."""

    cliente_nombre = fields.Str(required=True, validate=validate.Length(min=2, max=100))
    cliente_contacto = fields.Str(required=True, validate=validate.Length(min=7, max=20))
    fecha = fields.Date(required=True)
    hora = fields.Time(required=True)
    num_personas = fields.Int(required=True, validate=validate.Range(min=1, max=30))
    tipo_ocasion = fields.Str(required=True, validate=validate.OneOf(TIPOS_OCASION))


class ReservaEstadoSchema(Schema):
    """Schema para actualización de estado de reserva."""

    estado = fields.Str(required=True, validate=validate.OneOf(ESTADOS_RESERVA))


class ReservaCancelarSchema(Schema):
    """Schema para cancelación de reserva por código."""

    codigo_confirmacion = fields.Str(required=True, validate=validate.Length(min=5, max=20))


class ReservaDisponibilidadSchema(Schema):
    """Schema para consulta de disponibilidad (query params)."""

    fecha = fields.Date(required=True)
    hora = fields.Time(required=False, load_default=None)
    tipo_ocasion = fields.Str(required=True, validate=validate.OneOf(TIPOS_OCASION))
    num_personas = fields.Int(required=True, validate=validate.Range(min=1, max=30))
