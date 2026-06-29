"""Modelos SQLAlchemy del sistema."""
from app.models.usuario import Usuario
from app.models.mesa import Mesa
from app.models.reserva import Reserva
from app.models.categoria import Categoria
from app.models.platillo import Platillo
from app.models.pedido_takeaway import PedidoTakeaway
from app.models.detalle_pedido import DetallePedido
from app.models.configuracion import Configuracion

__all__ = [
    "Usuario",
    "Mesa",
    "Reserva",
    "Categoria",
    "Platillo",
    "PedidoTakeaway",
    "DetallePedido",
    "Configuracion",
]
