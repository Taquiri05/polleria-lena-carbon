# =============================================================================
# backend/tests/unit/test_admin_service.py
# Pruebas unitarias del servicio de administración
# Pollería Leña y Carbón — IS-489 UNSCH 2026
# =============================================================================

import pytest
from app.services.admin_service import (
    obtener_dashboard,
    obtener_configuracion,
    actualizar_configuracion,
)
from app.utils.exceptions import ServiceError


class TestObtenerDashboard:
    """Pruebas para obtener_dashboard()."""

    def test_dashboard_vacio(self, app):
        """Dashboard sin datos debe retornar ceros."""
        with app.app_context():
            resultado = obtener_dashboard()
            assert resultado["reservas_hoy"] == 0
            assert resultado["pedidos_hoy"] == 0
            assert resultado["ingresos_estimados"] == 0.0
            assert isinstance(resultado["platillos_top"], list)

    def test_dashboard_con_reserva(self, app, reserva_pendiente):
        """Dashboard debe contar reservas del día."""
        with app.app_context():
            resultado = obtener_dashboard()
            assert isinstance(resultado["reservas_hoy"], int)

    def test_dashboard_con_pedido(self, app, pedido_takeaway):
        """Dashboard debe contar pedidos del día."""
        with app.app_context():
            resultado = obtener_dashboard()
            assert resultado["pedidos_hoy"] >= 1

    def test_dashboard_retorna_estructura_correcta(self, app):
        """Dashboard debe retornar todas las claves esperadas."""
        with app.app_context():
            resultado = obtener_dashboard()
            assert "reservas_hoy" in resultado
            assert "pedidos_hoy" in resultado
            assert "ingresos_estimados" in resultado
            assert "platillos_top" in resultado


class TestObtenerConfiguracion:
    """Pruebas para obtener_configuracion()."""

    def test_obtener_configuracion_vacia(self, app):
        """Debe retornar diccionario vacío si no hay configuración."""
        with app.app_context():
            resultado = obtener_configuracion()
            assert isinstance(resultado, dict)

    def test_obtener_configuracion_con_datos(self, app, session):
        """Debe retornar configuración existente."""
        with app.app_context():
            from app.models.configuracion import Configuracion

            config = Configuracion(clave="nombre_negocio", valor="Pollería Test")
            session.add(config)
            session.commit()
            resultado = obtener_configuracion()
            assert resultado["nombre_negocio"] == "Pollería Test"


class TestActualizarConfiguracion:
    """Pruebas para actualizar_configuracion()."""

    def test_actualizar_configuracion_dict(self, app, session):
        """Debe actualizar configuración con dict clave-valor."""
        with app.app_context():
            from app.models.configuracion import Configuracion

            config = Configuracion(clave="nombre_negocio", valor="Original")
            session.add(config)
            session.commit()
            actualizar_configuracion({"nombre_negocio": "Nuevo Nombre"})
            resultado = obtener_configuracion()
            assert resultado["nombre_negocio"] == "Nuevo Nombre"

    def test_actualizar_configuracion_lista(self, app, session):
        """Debe actualizar configuración con lista de items."""
        with app.app_context():
            from app.models.configuracion import Configuracion

            config = Configuracion(clave="horario_apertura", valor="12:00")
            session.add(config)
            session.commit()
            actualizar_configuracion([{"clave": "horario_apertura", "valor": "11:00"}])
            resultado = obtener_configuracion()
            assert resultado["horario_apertura"] == "11:00"

    def test_actualizar_configuracion_clave_invalida(self, app):
        """Debe lanzar ServiceError 400 con clave no permitida."""
        with app.app_context():
            with pytest.raises(ServiceError) as exc:
                actualizar_configuracion({"clave_invalida": "valor"})
            assert exc.value.status_code == 400

    def test_crear_configuracion_nueva(self, app):
        """Debe crear configuración si no existe."""
        with app.app_context():
            actualizar_configuracion({"moneda": "PEN"})
            resultado = obtener_configuracion()
            assert resultado["moneda"] == "PEN"
