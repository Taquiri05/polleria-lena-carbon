"""Servicios del panel de administración."""
from datetime import date, datetime

from sqlalchemy import func

from app.extensions import db
from app.models.configuracion import Configuracion
from app.models.detalle_pedido import DetallePedido
from app.models.pedido_takeaway import PedidoTakeaway
from app.models.platillo import Platillo
from app.models.reserva import Reserva
from app.utils.exceptions import ServiceError


def obtener_dashboard() -> dict:
    """Métricas del día para el panel admin (RF-21)."""
    hoy = date.today()
    inicio = datetime.combine(hoy, datetime.min.time())
    fin = datetime.combine(hoy, datetime.max.time())

    reservas_hoy = Reserva.query.filter(
        Reserva.fecha == hoy,
        Reserva.estado != "cancelada",
    ).count()

    pedidos_hoy = PedidoTakeaway.query.filter(
        PedidoTakeaway.created_at.between(inicio, fin),
        PedidoTakeaway.estado != "cancelado",
    ).count()

    ingresos = (
        db.session.query(func.coalesce(func.sum(PedidoTakeaway.total), 0))
        .filter(
            PedidoTakeaway.created_at.between(inicio, fin),
            PedidoTakeaway.estado.notin_(["cancelado", "recibido"]),
        )
        .scalar()
    )

    platillos_top = (
        db.session.query(
            Platillo.nombre,
            func.sum(DetallePedido.cantidad).label("total_pedido"),
        )
        .join(DetallePedido, DetallePedido.platillo_id == Platillo.id)
        .join(PedidoTakeaway, DetallePedido.pedido_id == PedidoTakeaway.id)
        .filter(
            PedidoTakeaway.estado != "cancelado",
            PedidoTakeaway.created_at.between(inicio, fin),
        )
        .group_by(Platillo.id, Platillo.nombre)
        .order_by(func.sum(DetallePedido.cantidad).desc())
        .limit(5)
        .all()
    )

    return {
        "reservas_hoy": reservas_hoy,
        "pedidos_hoy": pedidos_hoy,
        "ingresos_estimados": float(ingresos or 0),
        "platillos_top": [
            {"nombre": nombre, "total_pedido": int(total)}
            for nombre, total in platillos_top
        ],
    }


def obtener_configuracion() -> dict:
    """Obtiene toda la configuración del sistema (RF-22)."""
    return Configuracion.get_all_dict()


def actualizar_configuracion(datos) -> None:
    """
    Actualiza parámetros de configuración (RF-22).
    Acepta un dict {clave: valor} o lista [{clave, valor}].
    """
    if isinstance(datos, list):
        items = datos
    elif isinstance(datos, dict) and "clave" in datos:
        items = [datos]
    else:
        items = [{"clave": k, "valor": str(v)} for k, v in datos.items()]

    for item in items:
        clave = item.get("clave")
        valor = str(item.get("valor", ""))

        if clave not in Configuracion.CLAVES_PERMITIDAS:
            raise ServiceError(f"Clave de configuración no reconocida: {clave}", 400)

        config = Configuracion.query.filter_by(clave=clave).first()
        if config:
            config.valor = valor
        else:
            db.session.add(Configuracion(clave=clave, valor=valor))

    db.session.commit()
