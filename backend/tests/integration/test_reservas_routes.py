# =============================================================================
# backend/tests/integration/test_reservas_routes.py
# Pruebas de integración — endpoints /api/reservas
# Pollería Leña y Carbón — IS-489 UNSCH 2026
# =============================================================================

import pytest
from datetime import date, timedelta


FECHA_FUTURA = str(date.today() + timedelta(days=3))
HORA_PRUEBA = "19:00"


class TestCrearReservaEndpoint:
    """Pruebas para POST /api/reservas."""

    def test_crear_reserva_exitosa(self, client, mesa_familiar):
        """Debe crear reserva y retornar 201 con código."""
        respuesta = client.post(
            "/api/reservas",
            json={
                "cliente_nombre": "Pedro Rojas",
                "cliente_contacto": "912345678",
                "fecha": FECHA_FUTURA,
                "hora": HORA_PRUEBA,
                "num_personas": 4,
                "tipo_ocasion": "familiar",
            },
        )
        assert respuesta.status_code == 201
        datos = respuesta.get_json()
        assert "codigo_confirmacion" in datos
        assert datos["codigo_confirmacion"].startswith("POLL-")

    def test_crear_reserva_sin_mesa(self, client):
        """Debe retornar 409 si no hay mesa disponible."""
        respuesta = client.post(
            "/api/reservas",
            json={
                "cliente_nombre": "Ana Torres",
                "cliente_contacto": "987333444",
                "fecha": FECHA_FUTURA,
                "hora": HORA_PRUEBA,
                "num_personas": 4,
                "tipo_ocasion": "familiar",
            },
        )
        assert respuesta.status_code == 409

    def test_crear_reserva_fecha_pasada(self, client):
        """Debe retornar 400 con fecha pasada."""
        respuesta = client.post(
            "/api/reservas",
            json={
                "cliente_nombre": "Luis",
                "cliente_contacto": "987000000",
                "fecha": str(date.today() - timedelta(days=1)),
                "hora": HORA_PRUEBA,
                "num_personas": 4,
                "tipo_ocasion": "familiar",
            },
        )
        assert respuesta.status_code == 400

    def test_crear_reserva_datos_faltantes(self, client):
        """Debe retornar 400 con datos incompletos."""
        respuesta = client.post("/api/reservas", json={"cliente_nombre": "Test"})
        assert respuesta.status_code == 400


class TestDisponibilidadEndpoint:
    """Pruebas para GET /api/reservas/disponibilidad."""

    def test_disponibilidad_con_mesa(self, client, mesa_familiar):
        """Debe retornar disponible True si hay mesa."""
        respuesta = client.get(
            f"/api/reservas/disponibilidad?fecha={FECHA_FUTURA}"
            f"&hora={HORA_PRUEBA}&tipo_ocasion=familiar&num_personas=4"
        )
        assert respuesta.status_code == 200
        datos = respuesta.get_json()
        assert "disponible" in datos
        assert datos["disponible"] is True

    def test_disponibilidad_sin_mesa(self, client):
        """Debe retornar disponible False sin mesas."""
        respuesta = client.get(
            f"/api/reservas/disponibilidad?fecha={FECHA_FUTURA}"
            f"&hora={HORA_PRUEBA}&tipo_ocasion=familiar&num_personas=4"
        )
        assert respuesta.status_code == 200
        datos = respuesta.get_json()
        assert datos["disponible"] is False


class TestListarReservasEndpoint:
    """Pruebas para GET /api/reservas."""

    def test_listar_sin_token(self, client):
        """Debe retornar 401 sin token."""
        respuesta = client.get("/api/reservas")
        assert respuesta.status_code == 401

    def test_listar_con_token_admin(self, client, token_admin, usuario_admin):
        """Admin debe poder listar reservas."""
        respuesta = client.get("/api/reservas", headers=token_admin)
        assert respuesta.status_code == 200
        assert isinstance(respuesta.get_json(), list)

    def test_listar_con_token_recepcionista(
        self, client, token_recepcionista, usuario_recepcionista
    ):
        """Recepcionista debe poder listar reservas."""
        respuesta = client.get("/api/reservas", headers=token_recepcionista)
        assert respuesta.status_code == 200


class TestActualizarEstadoReservaEndpoint:
    """Pruebas para PATCH /api/reservas/:id/estado."""

    def test_confirmar_reserva(
        self, client, token_admin, usuario_admin, reserva_pendiente
    ):
        """Admin debe poder confirmar una reserva."""
        from app.models.reserva import Reserva

        with client.application.app_context():
            reserva = Reserva.query.filter_by(codigo_confirmacion="POLL-TEST1").first()
            respuesta = client.patch(
                f"/api/reservas/{reserva.id}/estado",
                headers=token_admin,
                json={"estado": "confirmada"},
            )
        assert respuesta.status_code == 200
        assert respuesta.get_json()["estado"] == "confirmada"

    def test_actualizar_estado_sin_token(self, client):
        """Debe retornar 401 sin token."""
        respuesta = client.patch(
            "/api/reservas/1/estado", json={"estado": "confirmada"}
        )
        assert respuesta.status_code == 401


class TestCancelarReservaEndpoint:
    """Pruebas para POST /api/reservas/cancelar."""

    def test_cancelar_reserva_exitosa(self, client, reserva_pendiente):
        """Debe cancelar reserva con código válido."""
        respuesta = client.post(
            "/api/reservas/cancelar", json={"codigo_confirmacion": "POLL-TEST1"}
        )
        assert respuesta.status_code == 200
        assert "message" in respuesta.get_json()

    def test_cancelar_codigo_inexistente(self, client):
        """Debe retornar 404 con código inexistente."""
        respuesta = client.post(
            "/api/reservas/cancelar", json={"codigo_confirmacion": "POLL-NOEXISTE"}
        )
        assert respuesta.status_code == 404
