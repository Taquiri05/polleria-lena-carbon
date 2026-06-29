# =============================================================================
# backend/tests/unit/test_mesa_service.py
# Pruebas unitarias del servicio de mesas
# Pollería Leña y Carbón — IS-489 UNSCH 2026
# =============================================================================

import pytest
from app.services.mesa_service import (
    listar_mesas,
    obtener_mesa,
    crear_mesa,
    actualizar_mesa,
    cambiar_estado_mesa,
)
from app.utils.exceptions import ServiceError


class TestListarMesas:
    """Pruebas para listar_mesas()."""

    def test_listar_mesas_vacio(self, app):
        """Debe retornar lista vacía si no hay mesas."""
        with app.app_context():
            resultado = listar_mesas()
            assert isinstance(resultado, list)
            assert len(resultado) == 0

    def test_listar_mesas_activas(self, app, mesa_familiar):
        """Debe retornar solo mesas activas por defecto."""
        with app.app_context():
            resultado = listar_mesas()
            assert len(resultado) >= 1

    def test_listar_todas_las_mesas(self, app, session):
        """Debe retornar todas las mesas incluyendo inactivas."""
        with app.app_context():
            from app.models.mesa import Mesa

            mesa = Mesa(numero=99, capacidad=4, tipo_ocasion="familiar", activo=False)
            session.add(mesa)
            session.commit()
            resultado = listar_mesas(solo_activas=False)
            assert len(resultado) >= 1


class TestObtenerMesa:
    """Pruebas para obtener_mesa()."""

    def test_obtener_mesa_exitosa(self, app, mesa_familiar):
        """Debe retornar la mesa por ID."""
        with app.app_context():
            from app.models.mesa import Mesa

            mesa = Mesa.query.filter_by(numero=1).first()
            resultado = obtener_mesa(mesa.id)
            assert resultado.numero == 1

    def test_obtener_mesa_inexistente(self, app):
        """Debe lanzar ServiceError 404 si no existe."""
        with app.app_context():
            with pytest.raises(ServiceError) as exc:
                obtener_mesa(9999)
            assert exc.value.status_code == 404


class TestCrearMesa:
    """Pruebas para crear_mesa()."""

    def test_crear_mesa_exitosa(self, app):
        """Debe crear una mesa correctamente."""
        with app.app_context():
            datos = {"numero": 10, "capacidad": 4, "tipo_ocasion": "familiar"}
            resultado = crear_mesa(datos)
            assert resultado["numero"] == 10
            assert resultado["capacidad"] == 4

    def test_crear_mesa_numero_duplicado(self, app, mesa_familiar):
        """Debe lanzar ServiceError 409 con número duplicado."""
        with app.app_context():
            datos = {"numero": 1, "capacidad": 4, "tipo_ocasion": "familiar"}
            with pytest.raises(ServiceError) as exc:
                crear_mesa(datos)
            assert exc.value.status_code == 409

    def test_crear_mesa_romantica(self, app):
        """Debe crear mesa romántica correctamente."""
        with app.app_context():
            datos = {"numero": 5, "capacidad": 2, "tipo_ocasion": "romantica"}
            resultado = crear_mesa(datos)
            assert resultado["tipo_ocasion"] == "romantica"

    def test_crear_mesa_reunion(self, app):
        """Debe crear mesa de reunión correctamente."""
        with app.app_context():
            datos = {"numero": 6, "capacidad": 8, "tipo_ocasion": "reunion"}
            resultado = crear_mesa(datos)
            assert resultado["tipo_ocasion"] == "reunion"


class TestActualizarMesa:
    """Pruebas para actualizar_mesa()."""

    def test_actualizar_capacidad(self, app, mesa_familiar):
        """Debe actualizar la capacidad de la mesa."""
        with app.app_context():
            from app.models.mesa import Mesa

            mesa = Mesa.query.filter_by(numero=1).first()
            resultado = actualizar_mesa(mesa.id, {"capacidad": 8})
            assert resultado["capacidad"] == 8

    def test_actualizar_numero_duplicado(self, app, session):
        """Debe lanzar ServiceError 409 con número duplicado."""
        with app.app_context():
            from app.models.mesa import Mesa

            mesa1 = Mesa(numero=10, capacidad=4, tipo_ocasion="familiar", activo=True)
            mesa2 = Mesa(numero=11, capacidad=4, tipo_ocasion="familiar", activo=True)
            session.add_all([mesa1, mesa2])
            session.commit()
            with pytest.raises(ServiceError) as exc:
                actualizar_mesa(mesa2.id, {"numero": 10})
            assert exc.value.status_code == 409

    def test_actualizar_mesa_inexistente(self, app):
        """Debe lanzar ServiceError 404 si no existe."""
        with app.app_context():
            with pytest.raises(ServiceError) as exc:
                actualizar_mesa(9999, {"capacidad": 4})
            assert exc.value.status_code == 404


class TestCambiarEstadoMesa:
    """Pruebas para cambiar_estado_mesa()."""

    def test_desactivar_mesa(self, app, mesa_familiar):
        """Debe desactivar una mesa activa."""
        with app.app_context():
            from app.models.mesa import Mesa

            mesa = Mesa.query.filter_by(numero=1).first()
            cambiar_estado_mesa(mesa.id, False)
            mesa = Mesa.query.filter_by(numero=1).first()
            assert mesa.activo is False

    def test_activar_mesa(self, app, session):
        """Debe activar una mesa inactiva."""
        with app.app_context():
            from app.models.mesa import Mesa

            mesa = Mesa(numero=20, capacidad=4, tipo_ocasion="familiar", activo=False)
            session.add(mesa)
            session.commit()
            mesa_id = mesa.id
            cambiar_estado_mesa(mesa_id, True)
            mesa = Mesa.query.get(mesa_id)
            assert mesa.activo is True

    def test_cambiar_estado_mesa_inexistente(self, app):
        """Debe lanzar ServiceError 404 si no existe."""
        with app.app_context():
            with pytest.raises(ServiceError) as exc:
                cambiar_estado_mesa(9999, False)
            assert exc.value.status_code == 404
