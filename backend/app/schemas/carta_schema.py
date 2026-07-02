"""Schemas Marshmallow para el módulo de carta digital."""
from marshmallow import Schema, fields, validate


class CategoriaCreateSchema(Schema):
    """Schema para creación de categoría."""

    nombre = fields.Str(required=True, validate=validate.Length(min=2, max=100))
    descripcion = fields.Str(allow_none=True)


class CategoriaUpdateSchema(Schema):
    """Schema para edición de categoría."""

    nombre = fields.Str(validate=validate.Length(min=2, max=100))
    descripcion = fields.Str(allow_none=True)


class PlatilloCreateSchema(Schema):
    """Schema para creación de platillo."""

    nombre = fields.Str(required=True, validate=validate.Length(min=2, max=150))
    descripcion = fields.Str(allow_none=True)
    precio = fields.Decimal(required=True, places=2, validate=validate.Range(min=0.01))
    imagen_url = fields.Str(allow_none=True, validate=validate.Length(max=500))
    categoria_id = fields.Int(required=True)


class PlatilloUpdateSchema(Schema):
    """Schema para edición parcial de platillo."""

    nombre = fields.Str(validate=validate.Length(min=2, max=150))
    descripcion = fields.Str(allow_none=True)
    precio = fields.Decimal(places=2, validate=validate.Range(min=0.01))
    imagen_url = fields.Str(allow_none=True, validate=validate.Length(max=500))
    categoria_id = fields.Int()


class PlatilloEstadoSchema(Schema):
    """Schema para activar/desactivar platillo."""

    activo = fields.Bool(required=True)
