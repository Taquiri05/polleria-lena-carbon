# =============================================================================
# backend/tests/integration/test_carta_routes.py
# Pruebas de integración — endpoints /api/categorias y /api/platillos
# Pollería Leña y Carbón — IS-489 UNSCH 2026
# =============================================================================

import pytest


class TestCategoriasEndpoint:
    """Pruebas para /api/categorias."""

    def test_listar_categorias_publico(self, client, categoria_pollos):
        """Debe listar categorías sin autenticación."""
        respuesta = client.get("/api/categorias")
        assert respuesta.status_code == 200
        assert isinstance(respuesta.get_json(), list)

    def test_listar_categorias_vacio(self, client):
        """Debe retornar lista vacía si no hay categorías."""
        respuesta = client.get("/api/categorias")
        assert respuesta.status_code == 200
        assert respuesta.get_json() == []

    def test_crear_categoria_exitosa(self, client, token_admin, usuario_admin):
        """Admin debe poder crear categoría."""
        respuesta = client.post(
            "/api/categorias",
            headers=token_admin,
            json={"nombre": "Ensaladas", "descripcion": "Ensaladas frescas"},
        )
        assert respuesta.status_code == 201
        assert respuesta.get_json()["nombre"] == "Ensaladas"

    def test_crear_categoria_sin_token(self, client):
        """Debe retornar 401 sin token."""
        respuesta = client.post("/api/categorias", json={"nombre": "Test"})
        assert respuesta.status_code == 401

    def test_crear_categoria_duplicada(
        self, client, token_admin, usuario_admin, categoria_pollos
    ):
        """Debe retornar 409 con nombre duplicado."""
        respuesta = client.post(
            "/api/categorias", headers=token_admin, json={"nombre": "Pollos a la Brasa"}
        )
        assert respuesta.status_code == 409

    def test_actualizar_categoria_exitosa(
        self, client, token_admin, usuario_admin, categoria_pollos
    ):
        """Admin debe poder actualizar categoría."""
        with client.application.app_context():
            from app.models.categoria import Categoria

            cat = Categoria.query.filter_by(nombre="Pollos a la Brasa").first()
            respuesta = client.put(
                f"/api/categorias/{cat.id}",
                headers=token_admin,
                json={"nombre": "Pollos Especiales"},
            )
        assert respuesta.status_code == 200

    def test_eliminar_categoria_sin_platillos(
        self, client, token_admin, usuario_admin, session
    ):
        """Admin debe poder eliminar categoría vacía."""
        with client.application.app_context():
            from app.models.categoria import Categoria

            cat = Categoria(nombre="Temporal", descripcion="", activo=True)
            session.add(cat)
            session.commit()
            cat_id = cat.id
            respuesta = client.delete(f"/api/categorias/{cat_id}", headers=token_admin)
        assert respuesta.status_code == 200

    def test_eliminar_categoria_con_platillos(
        self, client, token_admin, usuario_admin, categoria_pollos, platillo_visible
    ):
        """Debe retornar 409 al eliminar categoría con platillos activos."""
        with client.application.app_context():
            from app.models.categoria import Categoria

            cat = Categoria.query.filter_by(nombre="Pollos a la Brasa").first()
            respuesta = client.delete(f"/api/categorias/{cat.id}", headers=token_admin)
        assert respuesta.status_code == 409


class TestPlatillosEndpoint:
    """Pruebas para /api/platillos."""

    def test_listar_platillos_publico(self, client, platillo_visible):
        """Debe listar platillos sin autenticación."""
        respuesta = client.get("/api/platillos")
        assert respuesta.status_code == 200
        assert isinstance(respuesta.get_json(), list)

    def test_listar_solo_activos_publico(
        self, client, platillo_visible, platillo_oculto
    ):
        """Carta pública solo debe mostrar platillos activos."""
        respuesta = client.get("/api/platillos")
        assert respuesta.status_code == 200
        nombres = [p["nombre"] for p in respuesta.get_json()]
        assert "1/4 Pollo a la Brasa" in nombres
        assert "Promoción Interna" not in nombres

    def test_crear_platillo_exitoso(
        self, client, token_admin, usuario_admin, categoria_pollos
    ):
        """Admin debe poder crear platillo."""
        with client.application.app_context():
            from app.models.categoria import Categoria

            cat = Categoria.query.filter_by(nombre="Pollos a la Brasa").first()
            respuesta = client.post(
                "/api/platillos",
                headers=token_admin,
                json={
                    "nombre": "Pollo BBQ",
                    "descripcion": "Pollo con salsa BBQ",
                    "precio": 25.00,
                    "categoria_id": cat.id,
                },
            )
        assert respuesta.status_code == 201
        assert respuesta.get_json()["nombre"] == "Pollo BBQ"

    def test_crear_platillo_sin_token(self, client, categoria_pollos):
        """Debe retornar 401 sin token."""
        respuesta = client.post(
            "/api/platillos",
            json={
                "nombre": "Test",
                "precio": 10.00,
                "categoria_id": categoria_pollos.id,
            },
        )
        assert respuesta.status_code == 401

    def test_desactivar_platillo(
        self, client, token_admin, usuario_admin, platillo_visible
    ):
        """Admin debe poder desactivar platillo."""
        with client.application.app_context():
            from app.models.platillo import Platillo

            plat = Platillo.query.get(platillo_visible.id)
            respuesta = client.patch(
                f"/api/platillos/{plat.id}/estado",
                headers=token_admin,
                json={"activo": False},
            )
        assert respuesta.status_code == 200

    def test_desactivar_platillo_sin_token(self, client):
        """Debe retornar 401 sin token."""
        respuesta = client.patch("/api/platillos/1/estado", json={"activo": False})
        assert respuesta.status_code == 401

    def test_actualizar_platillo_exitoso(
        self, client, token_admin, usuario_admin, platillo_visible
    ):
        """Admin debe poder actualizar precio del platillo."""
        with client.application.app_context():
            from app.models.platillo import Platillo

            plat = Platillo.query.get(platillo_visible.id)
            respuesta = client.put(
                f"/api/platillos/{plat.id}", headers=token_admin, json={"precio": 45.00}
            )
        assert respuesta.status_code == 200
