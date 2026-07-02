"""Schemas Marshmallow para el módulo takeaway."""
from marshmallow import Schema, fields, validate


ESTADOS_PEDIDO = ("recibido", "en_preparacion", "listo", "entregado", "cancelado")


class ItemPedidoSchema(Schema):
    """Schema para un ítem del pedido takeaway."""

    platillo_id = fields.Int(required=True)
    cantidad = fields.Int(required=True, validate=validate.Range(min=1, max=99))


class TakeawayCreateSchema(Schema):
    """Schema para creación de pedido takeaway."""

    cliente_nombre = fields.Str(required=True, validate=validate.Length(min=2, max=100))
    cliente_contacto = fields.Str(required=True, validate=validate.Length(min=7, max=20))
    items = fields.List(
        fields.Nested(ItemPedidoSchema),
        required=True,
        validate=validate.Length(min=1),
    )


class TakeawayEstadoSchema(Schema):
    """Schema para actualización de estado del pedido."""

    estado = fields.Str(required=True, validate=validate.OneOf(ESTADOS_PEDIDO))
