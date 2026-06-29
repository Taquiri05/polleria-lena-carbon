# =============================================================================
# backend/tests/integration/test_takeaway_routes.py
# Pruebas de integración — endpoints /api/takeaway
# Pollería Leña y Carbón — IS-489 UNSCH 2026
# =============================================================================

import pytest


class TestCrearPedidoEndpoint:
    """Pruebas para POST /api/takeaway."""

    def test_crear_pedido_exitoso(self, client, platillo_visible):
        """Debe crear pedido y retornar 201 con código."""
        respuesta = client.post(
            "/api/takeaway",
            json={
                "cliente_nombre": "Juan Pérez",
                "cliente_contacto": "987654321",
                "items": [{"platillo_id": platillo_visible.id, "cantidad": 2}],
            },
        )
        assert respuesta.status_code == 201
        datos = respuesta.get_json()
        assert "codigo_seguimiento" in datos
        assert datos["codigo_seguimiento"].startswith("TW-")
        assert datos["estado"] == "recibido"

    def test_crear_pedido_carrito_vacio(self, client):
        """Debe retornar 400 con carrito vacío."""
        respuesta = client.post(
            "/api/takeaway",
            json={
                "cliente_nombre": "Ana Torres",
                "cliente_contacto": "987333444",
                "items": [],
            },
        )
        assert respuesta.status_code == 400

    def test_crear_pedido_platillo_inactivo(self, client, platillo_oculto):
        """Debe retornar 422 con platillo desactivado."""
        respuesta = client.post(
            "/api/takeaway",
            json={
                "cliente_nombre": "Pedro Rojas",
                "cliente_contacto": "912345678",
                "items": [{"platillo_id": platillo_oculto.id, "cantidad": 1}],
            },
        )
        assert respuesta.status_code == 422

    def test_crear_pedido_datos_faltantes(self, client):
        """Debe retornar 400 con datos incompletos."""
        respuesta = client.post("/api/takeaway", json={"cliente_nombre": "Test"})
        assert respuesta.status_code == 400


class TestConsultarEstadoEndpoint:
    """Pruebas para GET /api/takeaway/estado/:codigo."""

    def test_consultar_estado_exitoso(self, client, pedido_takeaway):
        """Debe retornar estado del pedido por código."""
        respuesta = client.get("/api/takeaway/estado/TW-TEST001")
        assert respuesta.status_code == 200
        datos = respuesta.get_json()
        assert datos["codigo_seguimiento"] == "TW-TEST001"
        assert datos["estado"] == "recibido"

    def test_consultar_codigo_inexistente(self, client):
        """Debe retornar 404 con código inexistente."""
        respuesta = client.get("/api/takeaway/estado/TW-NOEXISTE")
        assert respuesta.status_code == 404


class TestListarPedidosEndpoint:
    """Pruebas para GET /api/takeaway."""

    def test_listar_sin_token(self, client):
        """Debe retornar 401 sin token."""
        respuesta = client.get("/api/takeaway")
        assert respuesta.status_code == 401

    def test_listar_con_token_admin(self, client, token_admin, usuario_admin):
        """Admin debe poder listar pedidos."""
        respuesta = client.get("/api/takeaway", headers=token_admin)
        assert respuesta.status_code == 200
        assert isinstance(respuesta.get_json(), list)

    def test_listar_con_filtro_estado(
        self, client, token_admin, usuario_admin, pedido_takeaway
    ):
        """Debe filtrar pedidos por estado."""
        respuesta = client.get("/api/takeaway?estado=recibido", headers=token_admin)
        assert respuesta.status_code == 200
        datos = respuesta.get_json()
        assert all(p["estado"] == "recibido" for p in datos)


class TestActualizarEstadoPedidoEndpoint:
    """Pruebas para PATCH /api/takeaway/:id/estado."""

    def test_actualizar_estado_exitoso(
        self, client, token_admin, usuario_admin, pedido_takeaway
    ):
        """Admin debe poder actualizar estado del pedido."""
        with client.application.app_context():
            from app.models.pedido_takeaway import PedidoTakeaway

            pedido = PedidoTakeaway.query.filter_by(
                codigo_seguimiento="TW-TEST001"
            ).first()
            respuesta = client.patch(
                f"/api/takeaway/{pedido.id}/estado",
                headers=token_admin,
                json={"estado": "en_preparacion"},
            )
        assert respuesta.status_code == 200
        assert respuesta.get_json()["estado"] == "en_preparacion"

    def test_actualizar_estado_sin_token(self, client):
        """Debe retornar 401 sin token."""
        respuesta = client.patch(
            "/api/takeaway/1/estado", json={"estado": "en_preparacion"}
        )
        assert respuesta.status_code == 401

    def test_cancelar_pedido_en_preparacion(
        self, client, token_admin, usuario_admin, session
    ):
        """Debe retornar 422 al cancelar pedido en preparación."""
        with client.application.app_context():
            from app.models.pedido_takeaway import PedidoTakeaway

            pedido = PedidoTakeaway(
                cliente_nombre="Test",
                cliente_contacto="987000000",
                total=20.00,
                estado="en_preparacion",
                codigo_seguimiento="TW-PREP999",
            )
            session.add(pedido)
            session.commit()
            ped_id = pedido.id
            respuesta = client.patch(
                f"/api/takeaway/{ped_id}/estado",
                headers=token_admin,
                json={"estado": "cancelado"},
            )
        assert respuesta.status_code == 422
