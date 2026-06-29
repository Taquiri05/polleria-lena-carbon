"""Servicios del módulo de reservas — lógica crítica de negocio."""
from datetime import date, datetime, time, timedelta
from typing import Optional

from app.extensions import db
from app.models.configuracion import Configuracion
from app.models.mesa import Mesa
from app.models.reserva import Reserva
from app.utils.exceptions import ServiceError


def _obtener_bloqueo_horas() -> int:
    """Obtiene las horas de bloqueo de reserva desde configuración (RN-01)."""
    valor = Configuracion.get_valor("bloqueo_reserva_horas", "2")
    return int(valor)


def _obtener_cancelacion_min_horas() -> int:
    """Obtiene las horas mínimas de anticipación para cancelar (RF-07)."""
    valor = Configuracion.get_valor("cancelacion_min_horas", "1")
    return int(valor)


def _calcular_rango_bloqueo(fecha: date, hora: time) -> tuple[datetime, datetime]:
    """Calcula inicio y fin del tramo de bloqueo de 2 horas."""
    inicio = datetime.combine(fecha, hora)
    bloqueo = _obtener_bloqueo_horas()
    fin = inicio + timedelta(hours=bloqueo)
    return inicio, fin


def _reservas_activas_solapan(mesa_id: int, fecha: date, hora_inicio: time, hora_fin: time) -> bool:
    """Verifica si existen reservas activas que se solapen con el tramo horario."""
    reservas = Reserva.query.filter(
        Reserva.mesa_id == mesa_id,
        Reserva.fecha == fecha,
        Reserva.estado.notin_(["cancelada", "completada"]),
    ).all()

    inicio_nuevo, fin_nuevo = _calcular_rango_bloqueo(fecha, hora_inicio)
    # Usar hora_fin como referencia alternativa si se pasa explícitamente
    fin_nuevo = datetime.combine(fecha, hora_fin) if hora_fin else fin_nuevo

    for reserva in reservas:
        inicio_existente, fin_existente = _calcular_rango_bloqueo(reserva.fecha, reserva.hora)
        if inicio_existente < fin_nuevo and fin_existente > inicio_nuevo:
            return True
    return False


def validar_disponibilidad_mesa(mesa_id: int, fecha: date, hora: time) -> bool:
    """
    Verifica si una mesa específica está disponible en fecha/hora (RN-01).
    Retorna True si está libre, False si hay conflicto.
    """
    mesa = db.session.get(Mesa, mesa_id)
    if not mesa or not mesa.activo:
        return False

    inicio, fin = _calcular_rango_bloqueo(fecha, hora)
    return not _reservas_activas_solapan(mesa_id, fecha, hora, fin.time())


def asignar_mesa_automatica(
    fecha: date,
    hora: time,
    num_personas: int,
    tipo_ocasion: str,
) -> Optional[Mesa]:
    """
    Asigna automáticamente la mesa más adecuada (RN-01, RN-02, RN-03, RN-04).
    Prioriza: disponibilidad, tipo de ocasión compatible, capacidad mínima suficiente.
    """
    # Criterios de capacidad mínima según tipo de ocasión (RN-03)
    capacidad_minima = {
        "familiar": 4,
        "romantica": 2,
        "reunion": 6,
    }.get(tipo_ocasion, num_personas)

    capacidad_requerida = max(num_personas, capacidad_minima)

    mesas_candidatas = (
        Mesa.query.filter(
            Mesa.activo.is_(True),
            Mesa.tipo_ocasion == tipo_ocasion,
            Mesa.capacidad >= capacidad_requerida,
        )
        .order_by(Mesa.capacidad.asc())
        .all()
    )

    inicio, fin = _calcular_rango_bloqueo(fecha, hora)

    for mesa in mesas_candidatas:
        if not _reservas_activas_solapan(mesa.id, fecha, hora, fin.time()):
            return mesa

    return None


def consultar_disponibilidad(
    fecha: date,
    tipo_ocasion: str,
    num_personas: int,
    hora: Optional[time] = None,
) -> dict:
    """
    Consulta disponibilidad de mesas para una fecha y tipo de ocasión (RF-03).
    """
    if fecha < date.today():
        raise ServiceError("No se pueden consultar fechas pasadas.", 400, campo="fecha")

    if hora:
        mesa = asignar_mesa_automatica(fecha, hora, num_personas, tipo_ocasion)
        return {"disponible": mesa is not None}

    # Sugerir horarios disponibles en el rango operativo
    horarios_sugeridos = []
    hora_apertura = Configuracion.get_valor("horario_apertura", "12:00")
    hora_cierre = Configuracion.get_valor("horario_cierre", "22:00")

    try:
        h_inicio = datetime.strptime(hora_apertura, "%H:%M").time()
        h_fin = datetime.strptime(hora_cierre, "%H:%M").time()
    except ValueError:
        h_inicio = time(12, 0)
        h_fin = time(22, 0)

    actual = datetime.combine(fecha, h_inicio)
    limite = datetime.combine(fecha, h_fin)

    while actual <= limite:
        hora_slot = actual.time()
        mesa = asignar_mesa_automatica(fecha, hora_slot, num_personas, tipo_ocasion)
        if mesa:
            horarios_sugeridos.append(hora_slot.strftime("%H:%M"))
        actual += timedelta(minutes=30)

    return {
        "disponible": len(horarios_sugeridos) > 0,
        "horarios_sugeridos": horarios_sugeridos,
    }


def crear_reserva(datos: dict) -> dict:
    """
    Crea una reserva con asignación automática de mesa (RF-01, RF-02, RF-04).
    CU-01: Realizar Reserva.
    """
    fecha = datos["fecha"]
    hora = datos["hora"]

    if fecha < date.today():
        raise ServiceError("No se pueden crear reservas en fechas pasadas.", 400, campo="fecha")

    if fecha == date.today():
        ahora = datetime.now().time()
        if hora <= ahora:
            raise ServiceError("La hora de reserva debe ser futura.", 400, campo="hora")

    mesa = asignar_mesa_automatica(
        fecha, hora, datos["num_personas"], datos["tipo_ocasion"]
    )

    if not mesa:
        raise ServiceError(
            "No hay mesas disponibles para el horario y tipo de ocasión seleccionados.",
            409,
        )

    codigo = Reserva.generar_codigo()
    while Reserva.query.filter_by(codigo_confirmacion=codigo).first():
        codigo = Reserva.generar_codigo()

    reserva = Reserva(
        cliente_nombre=datos["cliente_nombre"],
        cliente_contacto=datos["cliente_contacto"],
        fecha=fecha,
        hora=hora,
        num_personas=datos["num_personas"],
        tipo_ocasion=datos["tipo_ocasion"],
        estado="pendiente",
        codigo_confirmacion=codigo,
        mesa_id=mesa.id,
    )
    db.session.add(reserva)
    db.session.commit()

    return {
        "id": reserva.id,
        "codigo_confirmacion": reserva.codigo_confirmacion,
        "mesa": {"numero": mesa.numero},
        "fecha": reserva.fecha.isoformat(),
        "hora": str(reserva.hora),
        "estado": reserva.estado,
    }


def listar_reservas(fecha: Optional[date] = None, estado: Optional[str] = None) -> list[dict]:
    """Lista reservas con filtros opcionales (RF-05)."""
    query = Reserva.query

    if fecha:
        query = query.filter_by(fecha=fecha)
    if estado:
        query = query.filter_by(estado=estado)

    reservas = query.order_by(Reserva.fecha, Reserva.hora).all()
    resultado = []
    for r in reservas:
        item = {
            "id": r.id,
            "cliente_nombre": r.cliente_nombre,
            "fecha": r.fecha.isoformat(),
            "hora": str(r.hora),
            "estado": r.estado,
            "codigo_confirmacion": r.codigo_confirmacion,
            "mesa": {"numero": r.mesa.numero} if r.mesa else None,
        }
        resultado.append(item)
    return resultado


def obtener_reserva(reserva_id: int) -> dict:
    """Obtiene el detalle de una reserva."""
    reserva = db.session.get(Reserva, reserva_id)
    if not reserva:
        raise ServiceError("Reserva no encontrada.", 404)
    return reserva.to_dict(include_mesa=True)


def actualizar_estado_reserva(reserva_id: int, nuevo_estado: str) -> dict:
    """Actualiza el estado de una reserva (RF-06)."""
    reserva = db.session.get(Reserva, reserva_id)
    if not reserva:
        raise ServiceError("Reserva no encontrada.", 404)

    if not reserva.puede_transicionar(nuevo_estado):
        raise ServiceError(
            f"Transición de estado inválida: {reserva.estado} → {nuevo_estado}.",
            422,
        )

    reserva.estado = nuevo_estado
    db.session.commit()
    return {"id": reserva.id, "estado": reserva.estado}


def cancelar_reserva_por_codigo(codigo_confirmacion: str) -> None:
    """
    Cancela una reserva por código de confirmación (RF-07).
    Requiere al menos 1 hora de anticipación.
    """
    reserva = Reserva.query.filter_by(codigo_confirmacion=codigo_confirmacion).first()
    if not reserva:
        raise ServiceError("Código de confirmación no encontrado.", 404)

    if reserva.estado in ("completada", "cancelada"):
        raise ServiceError("La reserva no puede ser cancelada en su estado actual.", 422)

    fecha_hora_reserva = datetime.combine(reserva.fecha, reserva.hora)
    minutos_restantes = (fecha_hora_reserva - datetime.now()).total_seconds() / 60
    min_horas = _obtener_cancelacion_min_horas()

    if minutos_restantes < min_horas * 60:
        raise ServiceError(
            f"La cancelación debe realizarse con al menos {min_horas} hora(s) de anticipación.",
            422,
        )

    reserva.estado = "cancelada"
    db.session.commit()
