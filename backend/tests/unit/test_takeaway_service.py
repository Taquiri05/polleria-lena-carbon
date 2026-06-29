# =============================================================================
# backend/tests/unit/test_takeaway_service.py
# Pruebas unitarias del servicio de takeaway
# Pollería Leña y Carbón — IS-489 UNSCH 2026
# =============================================================================

import pytest
from decimal import Decimal
from app.services.takeaway_service import (
    calcular_total_pedido,
    crear_pedido_takeaway,
    actualizar_estado_pedido,
    consultar_estado_por_codigo,
    listar_pedidos,
    obtener_pedido,
)
from app.utils.exceptions import ServiceError


class TestCalcularTotalPedido:
    """Pruebas para calcular_total_pedido() — función crítica #4."""

    def test_calcular_total_con_precio_unitario(self, app):
        """Debe calcular total correctamente con precio_unitario dado."""
        with app.app_context():
            items = [
                {"platillo_id": 1, "cantidad": 2, "precio_unitario": 38.50},
                {"platillo_id": 2, "cantidad": 1, "precio_unitario": 8.00},
            ]
            total = calcular_total_pedido(items)
            assert total == Decimal("85.00")

    def test_calcular_total_un_item(self, app):
        """Debe calcular total con un solo ítem."""
        with app.app_context():
            items = [{"platillo_id": 1, "cantidad": 2, "precio_unitario": 38.50}]
            total = calcular_total_pedido(items)
            assert total == Decimal("77.00")

    def test_calcular_total_desde_bd(self, app, platillo_visible):
        """Debe calcular total obteniendo precio desde la BD."""
        with app.app_context():
            items = [{"platillo_id": platillo_visible.id, "cantidad": 2}]
            total = calcular_total_pedido(items)
            assert total == Decimal("77.00")

    def test_calcular_total_platillo_inexistente(self, app):
        """Debe lanzar ServiceError 400 si el platillo no existe."""
        with app.app_context():
            items = [{"platillo_id": 9999, "cantidad": 1}]
            with pytest.raises(ServiceError) as exc:
                calcular_total_pedido(items)
            assert exc.value.status_code == 400


class TestCrearPedidoTakeaway:
    """Pruebas para crear_pedido_takeaway() — función crítica #5."""

    def test_crear_pedido_exitoso(self, app, platillo_visible):
        """Debe crear pedido y retornar código de seguimiento."""
        with app.app_context():
            datos = {
                "cliente_nombre": "Juan Pérez",
                "cliente_contacto": "987654321",
                "items": [{"platillo_id": platillo_visible.id, "cantidad": 2}],
            }
            resultado = crear_pedido_takeaway(datos)
            assert "codigo_seguimiento" in resultado
            assert resultado["codigo_seguimiento"].startswith("TW-")
            assert resultado["estado"] == "recibido"
            assert float(resultado["total"]) == 77.00

    def test_crear_pedido_carrito_vacio(self, app):
        """Debe lanzar ServiceError 400 si no hay ítems."""
        with app.app_context():
            datos = {
                "cliente_nombre": "Ana Torres",
                "cliente_contacto": "987333444",
                "items": [],
            }
            with pytest.raises(ServiceError) as exc:
                crear_pedido_takeaway(datos)
            assert exc.value.status_code == 400

    def test_crear_pedido_platillo_inactivo(self, app, platillo_oculto):
        """Debe lanzar ServiceError 422 con platillo desactivado."""
        with app.app_context():
            datos = {
                "cliente_nombre": "Pedro Rojas",
                "cliente_contacto": "912345678",
                "items": [{"platillo_id": platillo_oculto.id, "cantidad": 1}],
            }
            with pytest.raises(ServiceError) as exc:
                crear_pedido_takeaway(datos)
            assert exc.value.status_code == 422

    def test_crear_pedido_platillo_inexistente(self, app):
        """Debe lanzar ServiceError 400 con platillo que no existe."""
        with app.app_context():
            datos = {
                "cliente_nombre": "Luis García",
                "cliente_contacto": "987111000",
                "items": [{"platillo_id": 9999, "cantidad": 1}],
            }
            with pytest.raises(ServiceError) as exc:
                crear_pedido_takeaway(datos)
            assert exc.value.status_code == 400

    def test_crear_pedido_codigo_unico(self, app, platillo_visible):
        """Dos pedidos deben tener códigos diferentes."""
        with app.app_context():
            datos = {
                "cliente_nombre": "Cliente A",
                "cliente_contacto": "987000001",
                "items": [{"platillo_id": platillo_visible.id, "cantidad": 1}],
            }
            pedido1 = crear_pedido_takeaway(datos)
            datos["cliente_nombre"] = "Cliente B"
            datos["cliente_contacto"] = "987000002"
            pedido2 = crear_pedido_takeaway(datos)
            assert pedido1["codigo_seguimiento"] != pedido2["codigo_seguimiento"]


class TestActualizarEstadoPedido:
    """Pruebas para actualizar_estado_pedido() — función crítica #6."""

    def test_avanzar_estado_recibido_a_preparacion(self, app, pedido_takeaway):
        """Debe avanzar de recibido a en_preparacion."""
        with app.app_context():
            from app.models.pedido_takeaway import PedidoTakeaway

            pedido = PedidoTakeaway.query.filter_by(
                codigo_seguimiento="TW-TEST001"
            ).first()
            resultado = actualizar_estado_pedido(pedido.id, "en_preparacion")
            assert resultado["estado"] == "en_preparacion"

    def test_cancelar_desde_recibido(self, app, pedido_takeaway):
        """Debe cancelar pedido en estado recibido (RN-05)."""
        with app.app_context():
            from app.models.pedido_takeaway import PedidoTakeaway

            pedido = PedidoTakeaway.query.filter_by(
                codigo_seguimiento="TW-TEST001"
            ).first()
            resultado = actualizar_estado_pedido(pedido.id, "cancelado")
            assert resultado["estado"] == "cancelado"

    def test_cancelar_desde_preparacion_falla(self, app, session):
        """No debe cancelar pedido en preparación (RN-05)."""
        with app.app_context():
            from app.models.pedido_takeaway import PedidoTakeaway

            pedido = PedidoTakeaway(
                cliente_nombre="Test",
                cliente_contacto="987000000",
                total=20.00,
                estado="en_preparacion",
                codigo_seguimiento="TW-PREP001",
            )
            session.add(pedido)
            session.commit()
            ped_id = pedido.id
            with pytest.raises(ServiceError) as exc:
                actualizar_estado_pedido(ped_id, "cancelado")
            assert exc.value.status_code == 422

    def test_transicion_invalida(self, app, pedido_takeaway):
        """Debe lanzar ServiceError 422 con transición inválida."""
        with app.app_context():
            from app.models.pedido_takeaway import PedidoTakeaway

            pedido = PedidoTakeaway.query.filter_by(
                codigo_seguimiento="TW-TEST001"
            ).first()
            with pytest.raises(ServiceError) as exc:
                actualizar_estado_pedido(pedido.id, "entregado")
            assert exc.value.status_code == 422

    def test_pedido_inexistente(self, app):
        """Debe lanzar ServiceError 404 si el pedido no existe."""
        with app.app_context():
            with pytest.raises(ServiceError) as exc:
                actualizar_estado_pedido(9999, "en_preparacion")
            assert exc.value.status_code == 404


class TestConsultarEstadoPorCodigo:
    """Pruebas para consultar_estado_por_codigo()."""

    def test_consultar_estado_exitoso(self, app, pedido_takeaway):
        """Debe retornar estado del pedido por código."""
        with app.app_context():
            resultado = consultar_estado_por_codigo("TW-TEST001")
            assert resultado["estado"] == "recibido"
            assert resultado["codigo_seguimiento"] == "TW-TEST001"

    def test_consultar_codigo_inexistente(self, app):
        """Debe lanzar ServiceError 404 con código inexistente."""
        with app.app_context():
            with pytest.raises(ServiceError) as exc:
                consultar_estado_por_codigo("TW-NOEXISTE")
            assert exc.value.status_code == 404


class TestListarPedidos:
    """Pruebas para listar_pedidos()."""

    def test_listar_pedidos_vacio(self, app):
        """Debe retornar lista vacía si no hay pedidos."""
        with app.app_context():
            resultado = listar_pedidos()
            assert isinstance(resultado, list)
            assert len(resultado) == 0

    def test_listar_pedidos_con_datos(self, app, pedido_takeaway):
        """Debe retornar lista con el pedido creado."""
        with app.app_context():
            resultado = listar_pedidos()
            assert len(resultado) >= 1

    def test_listar_pedidos_filtro_estado(self, app, pedido_takeaway):
        """Debe filtrar pedidos por estado."""
        with app.app_context():
            resultado = listar_pedidos(estado="recibido")
            assert all(p["estado"] == "recibido" for p in resultado)
