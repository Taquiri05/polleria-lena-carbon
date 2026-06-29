# =============================================================================
# backend/tests/unit/test_carta_service.py
# Pruebas unitarias del servicio de carta digital
# Pollería Leña y Carbón — IS-489 UNSCH 2026
# =============================================================================

import pytest
from app.services.carta_service import (
    listar_categorias_publicas,
    listar_categorias_admin,
    crear_categoria,
    actualizar_categoria,
    eliminar_categoria,
    listar_platillos_publicos,
    crear_platillo,
    actualizar_platillo,
    cambiar_visibilidad_platillo,
)
from app.utils.exceptions import ServiceError


class TestListarCategorias:
    """Pruebas para listar categorías."""

    def test_listar_categorias_publicas_vacio(self, app):
        """Debe retornar lista vacía si no hay categorías."""
        with app.app_context():
            resultado = listar_categorias_publicas()
            assert isinstance(resultado, list)
            assert len(resultado) == 0

    def test_listar_categorias_publicas_con_datos(self, app, categoria_pollos):
        """Debe retornar solo categorías activas."""
        with app.app_context():
            resultado = listar_categorias_publicas()
            assert len(resultado) >= 1

    def test_listar_categorias_admin(self, app, categoria_pollos):
        """Admin debe ver todas las categorías."""
        with app.app_context():
            resultado = listar_categorias_admin()
            assert len(resultado) >= 1


class TestCrearCategoria:
    """Pruebas para crear_categoria()."""

    def test_crear_categoria_exitosa(self, app):
        """Debe crear una categoría correctamente."""
        with app.app_context():
            datos = {"nombre": "Ensaladas", "descripcion": "Ensaladas frescas"}
            resultado = crear_categoria(datos)
            assert resultado["nombre"] == "Ensaladas"

    def test_crear_categoria_nombre_duplicado(self, app, categoria_pollos):
        """Debe lanzar ServiceError 409 con nombre duplicado."""
        with app.app_context():
            datos = {"nombre": "Pollos a la Brasa"}
            with pytest.raises(ServiceError) as exc:
                crear_categoria(datos)
            assert exc.value.status_code == 409

    def test_crear_categoria_sin_descripcion(self, app):
        """Debe crear categoría sin descripción opcional."""
        with app.app_context():
            datos = {"nombre": "Postres"}
            resultado = crear_categoria(datos)
            assert resultado["nombre"] == "Postres"


class TestActualizarCategoria:
    """Pruebas para actualizar_categoria()."""

    def test_actualizar_categoria_exitosa(self, app, categoria_pollos):
        """Debe actualizar el nombre de la categoría."""
        with app.app_context():
            from app.models.categoria import Categoria

            cat = Categoria.query.filter_by(nombre="Pollos a la Brasa").first()
            resultado = actualizar_categoria(cat.id, {"nombre": "Pollos Especiales"})
            assert resultado["nombre"] == "Pollos Especiales"

    def test_actualizar_categoria_inexistente(self, app):
        """Debe lanzar ServiceError 404 si no existe."""
        with app.app_context():
            with pytest.raises(ServiceError) as exc:
                actualizar_categoria(9999, {"nombre": "Test"})
            assert exc.value.status_code == 404

    def test_actualizar_categoria_nombre_duplicado(self, app, session):
        """Debe lanzar ServiceError 409 con nombre ya existente."""
        with app.app_context():
            from app.models.categoria import Categoria

            # Crear dos categorías
            cat1 = Categoria(nombre="Bebidas", descripcion="", activo=True)
            cat2 = Categoria(nombre="Postres", descripcion="", activo=True)
            session.add_all([cat1, cat2])
            session.commit()
            with pytest.raises(ServiceError) as exc:
                actualizar_categoria(cat2.id, {"nombre": "Bebidas"})
            assert exc.value.status_code == 409


class TestEliminarCategoria:
    """Pruebas para eliminar_categoria()."""

    def test_eliminar_categoria_sin_platillos(self, app, session):
        """Debe eliminar categoría vacía correctamente."""
        with app.app_context():
            from app.models.categoria import Categoria

            cat = Categoria(nombre="Temporal", descripcion="", activo=True)
            session.add(cat)
            session.commit()
            cat_id = cat.id
            eliminar_categoria(cat_id)
            assert session.get(Categoria, cat_id) is None

    def test_eliminar_categoria_con_platillos_activos(
        self, app, categoria_pollos, platillo_visible
    ):
        """Debe lanzar ServiceError 409 si tiene platillos activos (RN-09)."""
        with app.app_context():
            from app.models.categoria import Categoria

            cat = Categoria.query.filter_by(nombre="Pollos a la Brasa").first()
            with pytest.raises(ServiceError) as exc:
                eliminar_categoria(cat.id)
            assert exc.value.status_code == 409

    def test_eliminar_categoria_inexistente(self, app):
        """Debe lanzar ServiceError 404 si no existe."""
        with app.app_context():
            with pytest.raises(ServiceError) as exc:
                eliminar_categoria(9999)
            assert exc.value.status_code == 404


class TestCambiarVisibilidadPlatillo:
    """Pruebas para cambiar_visibilidad_platillo() — función crítica #8."""

    def test_desactivar_platillo_exitoso(self, app, platillo_visible):
        """Debe desactivar un platillo visible."""
        with app.app_context():
            from app.models.platillo import Platillo

            plat = Platillo.query.get(platillo_visible.id)
            cambiar_visibilidad_platillo(plat.id, False)
            plat = Platillo.query.get(platillo_visible.id)
            assert plat.activo is False

    def test_activar_platillo_exitoso(self, app, platillo_oculto):
        """Debe activar un platillo oculto."""
        with app.app_context():
            from app.models.platillo import Platillo

            plat = Platillo.query.get(platillo_oculto.id)
            cambiar_visibilidad_platillo(plat.id, True)
            plat = Platillo.query.get(platillo_oculto.id)
            assert plat.activo is True

    def test_cambiar_visibilidad_platillo_inexistente(self, app):
        """Debe lanzar ServiceError 404 si el platillo no existe."""
        with app.app_context():
            with pytest.raises(ServiceError) as exc:
                cambiar_visibilidad_platillo(9999, False)
            assert exc.value.status_code == 404

    def test_platillo_oculto_no_aparece_en_carta_publica(self, app, platillo_oculto):
        """Platillo desactivado no debe aparecer en carta pública."""
        with app.app_context():
            resultado = listar_platillos_publicos()
            nombres = [p["nombre"] for p in resultado]
            assert "Promoción Interna" not in nombres


class TestCrearPlatillo:
    """Pruebas para crear_platillo()."""

    def test_crear_platillo_exitoso(self, app, categoria_pollos):
        """Debe crear un platillo correctamente."""
        with app.app_context():
            from app.models.categoria import Categoria

            cat = Categoria.query.filter_by(nombre="Pollos a la Brasa").first()
            datos = {
                "nombre": "Pollo BBQ",
                "descripcion": "Pollo con salsa BBQ",
                "precio": 25.00,
                "categoria_id": cat.id,
            }
            resultado = crear_platillo(datos)
            assert resultado["nombre"] == "Pollo BBQ"
            assert resultado["precio"] == 25.00

    def test_crear_platillo_categoria_inexistente(self, app):
        """Debe lanzar ServiceError 404 con categoría inexistente."""
        with app.app_context():
            datos = {"nombre": "Platillo Test", "precio": 10.00, "categoria_id": 9999}
            with pytest.raises(ServiceError) as exc:
                crear_platillo(datos)
            assert exc.value.status_code == 404


class TestActualizarPlatillo:
    """Pruebas para actualizar_platillo()."""

    def test_actualizar_platillo_exitoso(self, app, platillo_visible):
        """Debe actualizar el precio del platillo."""
        with app.app_context():
            from app.models.platillo import Platillo

            plat = Platillo.query.get(platillo_visible.id)
            resultado = actualizar_platillo(plat.id, {"precio": 45.00})
            assert resultado["precio"] == 45.00

    def test_actualizar_platillo_inexistente(self, app):
        """Debe lanzar ServiceError 404 si no existe."""
        with app.app_context():
            with pytest.raises(ServiceError) as exc:
                actualizar_platillo(9999, {"precio": 10.00})
            assert exc.value.status_code == 404
