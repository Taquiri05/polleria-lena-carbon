"""Servicios del módulo takeaway — lógica crítica de pedidos."""
from datetime import date, datetime
from decimal import Decimal
from typing import Optional

from app.extensions import db
from app.models.detalle_pedido import DetallePedido
from app.models.pedido_takeaway import PedidoTakeaway
from app.models.platillo import Platillo
from app.utils.exceptions import ServiceError


def calcular_total_pedido(items: list[dict]) -> Decimal:
    """
    Calcula el total de un pedido a partir de ítems con precio unitario (RN-06).
    items: [{platillo_id, cantidad, precio_unitario?}]
    """
    total = Decimal("0.00")
    for item in items:
        cantidad = item["cantidad"]
        if "precio_unitario" in item:
            precio = Decimal(str(item["precio_unitario"]))
        else:
            platillo = db.session.get(Platillo, item["platillo_id"])
            if not platillo:
                raise ServiceError(f"Platillo {item['platillo_id']} no encontrado.", 400)
            precio = Decimal(str(platillo.precio))
        total += precio * cantidad
    return total.quantize(Decimal("0.01"))


def _validar_items_disponibles(items: list[dict]) -> list[dict]:
    """Valida que todos los platillos existan y estén activos."""
    items_validados = []
    for item in items:
        platillo = db.session.get(Platillo, item["platillo_id"])
        if not platillo:
            raise ServiceError(
                f"Platillo con id {item['platillo_id']} no encontrado.",
                400,
                campo="platillo_id",
            )
        if not platillo.activo:
            raise ServiceError(
                f"El platillo '{platillo.nombre}' no está disponible.",
                422,
                campo="platillo_id",
            )
        items_validados.append({
            "platillo_id": platillo.id,
            "cantidad": item["cantidad"],
            "precio_unitario": platillo.precio,
            "platillo": platillo,
        })
    return items_validados


def crear_pedido_takeaway(datos: dict) -> dict:
    """
    Crea un pedido takeaway con ítems y calcula total (RF-14, RF-15, RF-16).
    CU-03: Realizar Pedido Takeaway.
    """
    items = datos.get("items", [])
    if not items:
        raise ServiceError("El pedido debe contener al menos un platillo.", 400)

    items_validados = _validar_items_disponibles(items)
    total = calcular_total_pedido(items_validados)

    codigo = PedidoTakeaway.generar_codigo()
    while PedidoTakeaway.query.filter_by(codigo_seguimiento=codigo).first():
        codigo = PedidoTakeaway.generar_codigo()

    pedido = PedidoTakeaway(
        cliente_nombre=datos["cliente_nombre"],
        cliente_contacto=datos["cliente_contacto"],
        total=total,
        estado="recibido",
        codigo_seguimiento=codigo,
    )
    db.session.add(pedido)
    db.session.flush()

    for item in items_validados:
        detalle = DetallePedido(
            pedido_id=pedido.id,
            platillo_id=item["platillo_id"],
            cantidad=item["cantidad"],
            precio_unitario=item["precio_unitario"],
        )
        db.session.add(detalle)

    db.session.commit()
    return pedido.to_dict(include_detalles=True)


def consultar_estado_por_codigo(codigo: str) -> dict:
    """Consulta el estado de un pedido por código de seguimiento (RF-19)."""
    pedido = PedidoTakeaway.query.filter_by(codigo_seguimiento=codigo).first()
    if not pedido:
        raise ServiceError("Código de seguimiento no encontrado.", 404)
    return pedido.to_dict(include_detalles=True)


def listar_pedidos(
    fecha: Optional[date] = None,
    estado: Optional[str] = None,
) -> list[dict]:
    """Lista pedidos takeaway con filtros (RF-17)."""
    query = PedidoTakeaway.query

    if fecha:
        inicio = datetime.combine(fecha, datetime.min.time())
        fin = datetime.combine(fecha, datetime.max.time())
        query = query.filter(PedidoTakeaway.created_at.between(inicio, fin))
    if estado:
        query = query.filter_by(estado=estado)

    pedidos = query.order_by(PedidoTakeaway.created_at.desc()).all()
    return [
        {
            "id": p.id,
            "cliente_nombre": p.cliente_nombre,
            "total": float(p.total),
            "estado": p.estado,
            "codigo_seguimiento": p.codigo_seguimiento,
            "created_at": p.created_at.isoformat(),
        }
        for p in pedidos
    ]


def obtener_pedido(pedido_id: int) -> dict:
    """Obtiene el detalle completo de un pedido."""
    pedido = db.session.get(PedidoTakeaway, pedido_id)
    if not pedido:
        raise ServiceError("Pedido no encontrado.", 404)
    return pedido.to_dict(include_detalles=True)


def actualizar_estado_pedido(pedido_id: int, nuevo_estado: str) -> dict:
    """
    Actualiza el estado de un pedido takeaway (RF-18, RN-05).
    La cancelación solo es válida desde estado 'recibido'.
    """
    pedido = db.session.get(PedidoTakeaway, pedido_id)
    if not pedido:
        raise ServiceError("Pedido no encontrado.", 404)

    if nuevo_estado == "cancelado" and pedido.estado != "recibido":
        raise ServiceError(
            "Solo se puede cancelar un pedido en estado 'recibido'.",
            422,
        )

    if not pedido.puede_transicionar(nuevo_estado):
        raise ServiceError(
            f"Transición de estado inválida: {pedido.estado} → {nuevo_estado}.",
            422,
        )

    pedido.estado = nuevo_estado
    db.session.commit()
    return {"id": pedido.id, "estado": pedido.estado}
