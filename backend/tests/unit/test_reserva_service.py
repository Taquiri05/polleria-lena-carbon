# =============================================================================
# backend/tests/unit/test_reserva_service.py
# Pruebas unitarias del servicio de reservas
# Pollería Leña y Carbón — IS-489 UNSCH 2026
# =============================================================================

import pytest
from datetime import date, time, timedelta

from app.services.reserva_service import (
    asignar_mesa_automatica,
    validar_disponibilidad_mesa,
    crear_reserva,
    actualizar_estado_reserva,
    cancelar_reserva_por_codigo,
    listar_reservas,
)
from app.utils.exceptions import ServiceError


# Fecha futura para todas las pruebas
FECHA_FUTURA = date.today() + timedelta(days=3)
HORA_PRUEBA = time(19, 0)


class TestAsignarMesaAutomatica:
    """Pruebas para asignar_mesa_automatica() — función crítica #1."""

    def test_asignar_mesa_familiar_exitoso(self, app, mesa_familiar):
        """Debe asignar mesa familiar para 4 personas."""
        with app.app_context():
            resultado = asignar_mesa_automatica(
                FECHA_FUTURA, HORA_PRUEBA, 4, "familiar"
            )
            assert resultado is not None
            assert resultado.tipo_ocasion == "familiar"
            assert resultado.capacidad >= 4

    def test_asignar_mesa_romantica_exitoso(self, app, mesa_romantica):
        """Debe asignar mesa romántica para 2 personas."""
        with app.app_context():
            resultado = asignar_mesa_automatica(
                FECHA_FUTURA, HORA_PRUEBA, 2, "romantica"
            )
            assert resultado is not None
            assert resultado.tipo_ocasion == "romantica"

    def test_asignar_mesa_reunion_exitoso(self, app, mesa_reunion):
        """Debe asignar mesa de reunión para 6 personas."""
        with app.app_context():
            resultado = asignar_mesa_automatica(FECHA_FUTURA, HORA_PRUEBA, 6, "reunion")
            assert resultado is not None
            assert resultado.tipo_ocasion == "reunion"

    def test_asignar_mesa_sin_disponibilidad(self, app):
        """Debe retornar None si no hay mesas disponibles."""
        with app.app_context():
            resultado = asignar_mesa_automatica(
                FECHA_FUTURA, HORA_PRUEBA, 4, "familiar"
            )
            assert resultado is None

    def test_asignar_mesa_con_reserva_existente(self, app, mesa_familiar, session):
        """No debe asignar mesa que ya tiene reserva activa en ese horario."""
        with app.app_context():
            from app.models.reserva import Reserva

            # Crear reserva que ocupa la mesa
            reserva = Reserva(
                cliente_nombre="Cliente Test",
                cliente_contacto="987000000",
                fecha=FECHA_FUTURA,
                hora=HORA_PRUEBA,
                num_personas=4,
                tipo_ocasion="familiar",
                estado="pendiente",
                codigo_confirmacion="POLL-BLOCK1",
                mesa_id=mesa_familiar.id,
            )
            session.add(reserva)
            session.commit()
            # Intentar asignar mesa en el mismo horario
            resultado = asignar_mesa_automatica(
                FECHA_FUTURA, HORA_PRUEBA, 4, "familiar"
            )
            assert resultado is None

    def test_asignar_mesa_tipo_incorrecto(self, app, mesa_familiar):
        """No debe asignar mesa familiar para ocasión romántica."""
        with app.app_context():
            resultado = asignar_mesa_automatica(
                FECHA_FUTURA, HORA_PRUEBA, 2, "romantica"
            )
            assert resultado is None


class TestValidarDisponibilidadMesa:
    """Pruebas para validar_disponibilidad_mesa() — función crítica #7."""

    def test_mesa_disponible(self, app, mesa_familiar):
        """Mesa sin reservas debe estar disponible."""
        with app.app_context():
            resultado = validar_disponibilidad_mesa(
                mesa_familiar.id, FECHA_FUTURA, HORA_PRUEBA
            )
            assert resultado is True

    def test_mesa_no_disponible_con_reserva(self, app, mesa_familiar, session):
        """Mesa con reserva activa no debe estar disponible."""
        with app.app_context():
            from app.models.reserva import Reserva

            reserva = Reserva(
                cliente_nombre="Ocupado",
                cliente_contacto="987000001",
                fecha=FECHA_FUTURA,
                hora=HORA_PRUEBA,
                num_personas=4,
                tipo_ocasion="familiar",
                estado="confirmada",
                codigo_confirmacion="POLL-OCP01",
                mesa_id=mesa_familiar.id,
            )
            session.add(reserva)
            session.commit()
            resultado = validar_disponibilidad_mesa(
                mesa_familiar.id, FECHA_FUTURA, HORA_PRUEBA
            )
            assert resultado is False

    def test_mesa_inexistente(self, app):
        """Mesa inexistente debe retornar False."""
        with app.app_context():
            resultado = validar_disponibilidad_mesa(9999, FECHA_FUTURA, HORA_PRUEBA)
            assert resultado is False

    def test_mesa_inactiva(self, app, session):
        """Mesa inactiva debe retornar False."""
        with app.app_context():
            from app.models.mesa import Mesa

            mesa = Mesa(numero=99, capacidad=4, tipo_ocasion="familiar", activo=False)
            session.add(mesa)
            session.commit()
            resultado = validar_disponibilidad_mesa(mesa.id, FECHA_FUTURA, HORA_PRUEBA)
            assert resultado is False


class TestCrearReserva:
    """Pruebas para crear_reserva() — función crítica #2."""

    def test_crear_reserva_exitosa(self, app, mesa_familiar):
        """Debe crear reserva y retornar código de confirmación."""
        with app.app_context():
            datos = {
                "cliente_nombre": "Pedro Rojas",
                "cliente_contacto": "912345678",
                "fecha": FECHA_FUTURA,
                "hora": HORA_PRUEBA,
                "num_personas": 4,
                "tipo_ocasion": "familiar",
            }
            resultado = crear_reserva(datos)
            assert "codigo_confirmacion" in resultado
            assert resultado["codigo_confirmacion"].startswith("POLL-")
            assert resultado["estado"] == "pendiente"

    def test_crear_reserva_sin_mesa_disponible(self, app):
        """Debe lanzar ServiceError 409 si no hay mesa disponible."""
        with app.app_context():
            datos = {
                "cliente_nombre": "Ana Torres",
                "cliente_contacto": "987333444",
                "fecha": FECHA_FUTURA,
                "hora": HORA_PRUEBA,
                "num_personas": 4,
                "tipo_ocasion": "familiar",
            }
            with pytest.raises(ServiceError) as exc:
                crear_reserva(datos)
            assert exc.value.status_code == 409

    def test_crear_reserva_fecha_pasada(self, app):
        """Debe lanzar ServiceError 400 con fecha pasada."""
        with app.app_context():
            datos = {
                "cliente_nombre": "Luis",
                "cliente_contacto": "987000000",
                "fecha": date.today() - timedelta(days=1),
                "hora": HORA_PRUEBA,
                "num_personas": 4,
                "tipo_ocasion": "familiar",
            }
            with pytest.raises(ServiceError) as exc:
                crear_reserva(datos)
            assert exc.value.status_code == 400


class TestActualizarEstadoReserva:
    """Pruebas para actualizar_estado_reserva()."""

    def test_confirmar_reserva_pendiente(self, app, reserva_pendiente):
        """Debe confirmar una reserva en estado pendiente."""
        with app.app_context():
            from app.models.reserva import Reserva

            reserva = Reserva.query.filter_by(codigo_confirmacion="POLL-TEST1").first()
            resultado = actualizar_estado_reserva(reserva.id, "confirmada")
            assert resultado["estado"] == "confirmada"

    def test_transicion_invalida(self, app, reserva_pendiente):
        """Debe lanzar ServiceError 422 con transición inválida."""
        with app.app_context():
            from app.models.reserva import Reserva

            reserva = Reserva.query.filter_by(codigo_confirmacion="POLL-TEST1").first()
            with pytest.raises(ServiceError) as exc:
                actualizar_estado_reserva(reserva.id, "completada")
            assert exc.value.status_code == 422

    def test_reserva_inexistente(self, app):
        """Debe lanzar ServiceError 404 si la reserva no existe."""
        with app.app_context():
            with pytest.raises(ServiceError) as exc:
                actualizar_estado_reserva(9999, "confirmada")
            assert exc.value.status_code == 404


class TestCancelarReservaPorCodigo:
    """Pruebas para cancelar_reserva_por_codigo()."""

    def test_cancelar_reserva_exitosa(self, app, reserva_pendiente):
        """Debe cancelar reserva con código válido y anticipación suficiente."""
        with app.app_context():
            cancelar_reserva_por_codigo("POLL-TEST1")
            from app.models.reserva import Reserva

            reserva = Reserva.query.filter_by(codigo_confirmacion="POLL-TEST1").first()
            assert reserva.estado == "cancelada"

    def test_cancelar_codigo_inexistente(self, app):
        """Debe lanzar ServiceError 404 con código inexistente."""
        with app.app_context():
            with pytest.raises(ServiceError) as exc:
                cancelar_reserva_por_codigo("POLL-NOEXISTE")
            assert exc.value.status_code == 404


class TestListarReservas:
    """Pruebas para listar_reservas()."""

    def test_listar_reservas_vacio(self, app):
        """Debe retornar lista vacía si no hay reservas."""
        with app.app_context():
            resultado = listar_reservas()
            assert isinstance(resultado, list)
            assert len(resultado) == 0

    def test_listar_reservas_con_datos(self, app, reserva_pendiente):
        """Debe retornar lista con la reserva creada."""
        with app.app_context():
            resultado = listar_reservas()
            assert len(resultado) >= 1


class TestConsultarDisponibilidad:
    """Pruebas para consultar_disponibilidad() — líneas 111-140."""

    def test_consultar_disponibilidad_con_hora(self, app, mesa_familiar):
        """Debe retornar disponible True si hay mesa."""
        with app.app_context():
            from datetime import date, time, timedelta
            from app.services.reserva_service import consultar_disponibilidad

            fecha = date.today() + timedelta(days=5)
            resultado = consultar_disponibilidad(fecha, "familiar", 4, time(19, 0))
            assert resultado["disponible"] is True

    def test_consultar_disponibilidad_sin_mesa(self, app):
        """Debe retornar disponible False si no hay mesa."""
        with app.app_context():
            from datetime import date, time, timedelta
            from app.services.reserva_service import consultar_disponibilidad

            fecha = date.today() + timedelta(days=5)
            resultado = consultar_disponibilidad(fecha, "familiar", 4, time(19, 0))
            assert resultado["disponible"] is False

    def test_consultar_disponibilidad_fecha_pasada(self, app):
        """Debe lanzar ServiceError 400 con fecha pasada."""
        with app.app_context():
            from datetime import date, timedelta
            from app.services.reserva_service import consultar_disponibilidad

            with pytest.raises(ServiceError) as exc:
                consultar_disponibilidad(
                    date.today() - timedelta(days=1), "familiar", 4
                )
            assert exc.value.status_code == 400

    def test_consultar_horarios_sugeridos(self, app, mesa_familiar):
        """Debe retornar horarios sugeridos cuando hay disponibilidad."""
        with app.app_context():
            from datetime import date, timedelta
            from app.services.reserva_service import consultar_disponibilidad

            fecha = date.today() + timedelta(days=5)
            resultado = consultar_disponibilidad(fecha, "familiar", 4)
            assert "horarios_sugeridos" in resultado


class TestObtenerReserva:
    """Pruebas para obtener_reserva() — línea 174."""

    def test_obtener_reserva_exitosa(self, app, reserva_pendiente):
        """Debe retornar reserva por ID."""
        with app.app_context():
            from app.models.reserva import Reserva
            from app.services.reserva_service import obtener_reserva

            reserva = Reserva.query.filter_by(codigo_confirmacion="POLL-TEST1").first()
            resultado = obtener_reserva(reserva.id)
            assert resultado["codigo_confirmacion"] == "POLL-TEST1"

    def test_obtener_reserva_inexistente(self, app):
        """Debe lanzar ServiceError 404 si no existe."""
        with app.app_context():
            from app.services.reserva_service import obtener_reserva

            with pytest.raises(ServiceError) as exc:
                obtener_reserva(9999)
            assert exc.value.status_code == 404
