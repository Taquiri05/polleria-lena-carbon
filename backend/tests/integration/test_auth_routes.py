# =============================================================================
# backend/tests/integration/test_auth_routes.py
# Pruebas de integración — endpoints /api/auth
# Pollería Leña y Carbón — IS-489 UNSCH 2026
# =============================================================================

import pytest


class TestLoginEndpoint:
    """Pruebas de integración para POST /api/auth/login."""

    def test_login_exitoso_admin(self, client, usuario_admin):
        """Debe retornar token JWT con credenciales válidas."""
        respuesta = client.post(
            "/api/auth/login",
            json={"email": "admin@prueba.com", "password": "Admin123!"},
        )
        assert respuesta.status_code == 200
        datos = respuesta.get_json()
        assert "access_token" in datos
        assert datos["usuario"]["rol"] == "ADMIN"

    def test_login_exitoso_recepcionista(self, client, usuario_recepcionista):
        """Recepcionista debe poder iniciar sesión."""
        respuesta = client.post(
            "/api/auth/login",
            json={"email": "recep@prueba.com", "password": "Recep123!"},
        )
        assert respuesta.status_code == 200
        datos = respuesta.get_json()
        assert datos["usuario"]["rol"] == "RECEPCIONISTA"

    def test_login_credenciales_invalidas(self, client, usuario_admin):
        """Debe retornar 401 con credenciales incorrectas."""
        respuesta = client.post(
            "/api/auth/login",
            json={"email": "admin@prueba.com", "password": "wrongpassword"},
        )
        assert respuesta.status_code == 401
        assert "error" in respuesta.get_json()

    def test_login_email_inexistente(self, client):
        """Debe retornar 401 con email que no existe."""
        respuesta = client.post(
            "/api/auth/login",
            json={"email": "noexiste@prueba.com", "password": "cualquier"},
        )
        assert respuesta.status_code == 401

    def test_login_cuenta_inactiva(self, client, usuario_inactivo):
        """Debe retornar 403 con cuenta desactivada."""
        respuesta = client.post(
            "/api/auth/login",
            json={"email": "inactivo@prueba.com", "password": "Pass123!"},
        )
        assert respuesta.status_code == 403

    def test_login_datos_faltantes(self, client):
        """Debe retornar 400 con body vacío."""
        respuesta = client.post("/api/auth/login", json={})
        assert respuesta.status_code == 400


class TestLogoutEndpoint:
    """Pruebas de integración para POST /api/auth/logout."""

    def test_logout_exitoso(self, client, token_admin):
        """Debe cerrar sesión con token válido."""
        respuesta = client.post("/api/auth/logout", headers=token_admin)
        assert respuesta.status_code == 200
        assert "message" in respuesta.get_json()

    def test_logout_sin_token(self, client):
        """Debe retornar 401 sin token."""
        respuesta = client.post("/api/auth/logout")
        assert respuesta.status_code == 401


class TestPerfilEndpoint:
    """Pruebas de integración para GET /api/auth/perfil."""

    def test_perfil_exitoso(self, client, token_admin, usuario_admin):
        """Debe retornar perfil del usuario autenticado."""
        respuesta = client.get("/api/auth/perfil", headers=token_admin)
        assert respuesta.status_code == 200
        datos = respuesta.get_json()
        assert "email" in datos
        assert "rol" in datos

    def test_perfil_sin_token(self, client):
        """Debe retornar 401 sin token."""
        respuesta = client.get("/api/auth/perfil")
        assert respuesta.status_code == 401


class TestCambiarPasswordEndpoint:
    """Pruebas de integración para PUT /api/auth/cambiar-password."""

    def test_cambiar_password_exitoso(self, client, token_admin, usuario_admin):
        """Debe cambiar contraseña correctamente."""
        respuesta = client.put(
            "/api/auth/cambiar-password",
            headers=token_admin,
            json={"password_actual": "Admin123!", "password_nueva": "NuevoPass123!"},
        )
        assert respuesta.status_code == 200

    def test_cambiar_password_actual_incorrecta(
        self, client, token_admin, usuario_admin
    ):
        """Debe retornar 400 con contraseña actual incorrecta."""
        respuesta = client.put(
            "/api/auth/cambiar-password",
            headers=token_admin,
            json={"password_actual": "incorrecta", "password_nueva": "NuevoPass123!"},
        )
        assert respuesta.status_code == 400

    def test_cambiar_password_sin_token(self, client):
        """Debe retornar 401 sin token."""
        respuesta = client.put(
            "/api/auth/cambiar-password",
            json={"password_actual": "Admin123!", "password_nueva": "NuevoPass123!"},
        )
        assert respuesta.status_code == 401
