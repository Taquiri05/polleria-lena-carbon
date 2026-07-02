"""Schemas Marshmallow para el módulo de mesas."""
from marshmallow import Schema, fields, validate


TIPOS_OCASION = ("familiar", "romantica", "reunion")


class MesaCreateSchema(Schema):
    """Schema para registro de nueva mesa."""

    numero = fields.Int(required=True, validate=validate.Range(min=1, max=999))
    capacidad = fields.Int(required=True, validate=validate.Range(min=1, max=30))
    tipo_ocasion = fields.Str(required=True, validate=validate.OneOf(TIPOS_OCASION))


class MesaUpdateSchema(Schema):
    """Schema para edición parcial de mesa."""

    numero = fields.Int(validate=validate.Range(min=1, max=999))
    capacidad = fields.Int(validate=validate.Range(min=1, max=30))
    tipo_ocasion = fields.Str(validate=validate.OneOf(TIPOS_OCASION))


class MesaEstadoSchema(Schema):
    """Schema para activar/desactivar mesa."""

    activo = fields.Bool(required=True)
