"""Schemas Marshmallow para validación y serialización."""
from app.schemas.usuario_schema import (
    UsuarioSchema,
    UsuarioCreateSchema,
    UsuarioUpdateSchema,
    LoginSchema,
    CambiarPasswordSchema,
)
from app.schemas.reserva_schema import (
    ReservaCreateSchema,
    ReservaEstadoSchema,
    ReservaCancelarSchema,
    ReservaDisponibilidadSchema,
)
from app.schemas.mesa_schema import MesaCreateSchema, MesaUpdateSchema, MesaEstadoSchema
from app.schemas.carta_schema import (
    CategoriaCreateSchema,
    CategoriaUpdateSchema,
    PlatilloCreateSchema,
    PlatilloUpdateSchema,
    PlatilloEstadoSchema,
)
from app.schemas.takeaway_schema import (
    TakeawayCreateSchema,
    TakeawayEstadoSchema,
    ItemPedidoSchema,
)

__all__ = [
    "UsuarioSchema",
    "UsuarioCreateSchema",
    "UsuarioUpdateSchema",
    "LoginSchema",
    "CambiarPasswordSchema",
    "ReservaCreateSchema",
    "ReservaEstadoSchema",
    "ReservaCancelarSchema",
    "ReservaDisponibilidadSchema",
    "MesaCreateSchema",
    "MesaUpdateSchema",
    "MesaEstadoSchema",
    "CategoriaCreateSchema",
    "CategoriaUpdateSchema",
    "PlatilloCreateSchema",
    "PlatilloUpdateSchema",
    "PlatilloEstadoSchema",
    "TakeawayCreateSchema",
    "TakeawayEstadoSchema",
    "ItemPedidoSchema",
]
