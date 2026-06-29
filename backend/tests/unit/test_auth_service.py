# =============================================================================
# backend/tests/unit/test_auth_service.py
# Pruebas unitarias del servicio de autenticación
# Pollería Leña y Carbón — IS-489 UNSCH 2026
# =============================================================================

import pytest
from app.services.auth_service import (
    autenticar_usuario,
    cambiar_password,
    crear_usuario,
    cambiar_estado_usuario,
)
from app.utils.exceptions import ServiceError


class TestAutenticarUsuario:
    """Pruebas para la función autenticar_usuario()."""

    def test_login_exitoso_admin(self, app, usuario_admin):
        """Debe retornar token JWT y datos del usuario admin."""
        with app.app_context():
            resultado = autenticar_usuario("admin@prueba.com", "Admin123!")
            assert "access_token" in resultado
            assert resultado["usuario"]["email"] == "admin@prueba.com"
            assert resultado["usuario"]["rol"] == "ADMIN"

    def test_login_exitoso_recepcionista(self, app, usuario_recepcionista):
        """Debe retornar token JWT para el recepcionista."""
        with app.app_context():
            resultado = autenticar_usuario("recep@prueba.com", "Recep123!")
            assert "access_token" in resultado
            assert resultado["usuario"]["rol"] == "RECEPCIONISTA"

    def test_login_password_incorrecto(self, app, usuario_admin):
        """Debe lanzar ServiceError 401 con password incorrecto."""
        with app.app_context():
            with pytest.raises(ServiceError) as exc:
                autenticar_usuario("admin@prueba.com", "passwordMalo")
            assert exc.value.status_code == 401

    def test_login_email_inexistente(self, app):
        """Debe lanzar ServiceError 401 con email inexistente."""
        with app.app_context():
            with pytest.raises(ServiceError) as exc:
                autenticar_usuario("noexiste@prueba.com", "cualquier")
            assert exc.value.status_code == 401

    def test_login_cuenta_inactiva(self, app, usuario_inactivo):
        """Debe lanzar ServiceError 403 con cuenta desactivada."""
        with app.app_context():
            with pytest.raises(ServiceError) as exc:
                autenticar_usuario("inactivo@prueba.com", "Pass123!")
            assert exc.value.status_code == 403

    def test_login_retorna_id_usuario(self, app, usuario_admin):
        """El resultado debe incluir el ID del usuario."""
        with app.app_context():
            resultado = autenticar_usuario("admin@prueba.com", "Admin123!")
            assert "id" in resultado["usuario"]
            assert isinstance(resultado["usuario"]["id"], int)


class TestCambiarPassword:
    """Pruebas para la función cambiar_password()."""

    def test_cambiar_password_exitoso(self, app, usuario_admin):
        """Debe cambiar la contraseña correctamente."""
        with app.app_context():
            # Obtener ID dentro del contexto
            from app.models.usuario import Usuario

            admin = Usuario.query.filter_by(email="admin@prueba.com").first()
            cambiar_password(admin.id, "Admin123!", "NuevoPass123!")
            # Verificar que la nueva contraseña funciona
            resultado = autenticar_usuario("admin@prueba.com", "NuevoPass123!")
            assert "access_token" in resultado

    def test_cambiar_password_actual_incorrecta(self, app, usuario_admin):
        """Debe lanzar ServiceError 400 si la contraseña actual es incorrecta."""
        with app.app_context():
            from app.models.usuario import Usuario

            admin = Usuario.query.filter_by(email="admin@prueba.com").first()
            with pytest.raises(ServiceError) as exc:
                cambiar_password(admin.id, "passwordMalo", "NuevoPass123!")
            assert exc.value.status_code == 400

    def test_cambiar_password_usuario_inexistente(self, app):
        """Debe lanzar ServiceError 404 si el usuario no existe."""
        with app.app_context():
            with pytest.raises(ServiceError) as exc:
                cambiar_password(9999, "cualquier", "nueva")
            assert exc.value.status_code == 404


class TestCrearUsuario:
    """Pruebas para la función crear_usuario()."""

    def test_crear_usuario_exitoso(self, app):
        """Debe crear un nuevo usuario correctamente."""
        with app.app_context():
            datos = {
                "nombre": "Nuevo Staff",
                "email": "nuevo@prueba.com",
                "password": "Pass123!",
                "rol": "RECEPCIONISTA",
            }
            resultado = crear_usuario(datos)
            assert resultado["email"] == "nuevo@prueba.com"
            assert resultado["rol"] == "RECEPCIONISTA"

    def test_crear_usuario_email_duplicado(self, app, usuario_admin):
        """Debe lanzar ServiceError 409 con email duplicado."""
        with app.app_context():
            datos = {
                "nombre": "Otro Admin",
                "email": "admin@prueba.com",
                "password": "Pass123!",
                "rol": "ADMIN",
            }
            with pytest.raises(ServiceError) as exc:
                crear_usuario(datos)
            assert exc.value.status_code == 409


class TestCambiarEstadoUsuario:
    """Pruebas para activar y desactivar usuarios."""

    def test_desactivar_usuario(self, app, usuario_recepcionista):
        """Debe desactivar un usuario correctamente."""
        with app.app_context():
            from app.models.usuario import Usuario

            recep = Usuario.query.filter_by(email="recep@prueba.com").first()
            cambiar_estado_usuario(recep.id, False)
            with pytest.raises(ServiceError) as exc:
                autenticar_usuario("recep@prueba.com", "Recep123!")
            assert exc.value.status_code == 403

    def test_activar_usuario(self, app, usuario_inactivo):
        """Debe activar un usuario inactivo correctamente."""
        with app.app_context():
            from app.models.usuario import Usuario

            inactivo = Usuario.query.filter_by(email="inactivo@prueba.com").first()
            cambiar_estado_usuario(inactivo.id, True)
            resultado = autenticar_usuario("inactivo@prueba.com", "Pass123!")
            assert "access_token" in resultado


class TestObtenerPerfil:
    """Pruebas para obtener_perfil() — líneas 72-73."""

    def test_obtener_perfil_exitoso(self, app, usuario_admin):
        """Debe retornar perfil del usuario."""
        with app.app_context():
            from app.models.usuario import Usuario
            from app.services.auth_service import obtener_perfil

            admin = Usuario.query.filter_by(email="admin@prueba.com").first()
            resultado = obtener_perfil(admin.id)
            assert resultado["email"] == "admin@prueba.com"
            assert resultado["rol"] == "ADMIN"

    def test_obtener_perfil_inexistente(self, app):
        """Debe lanzar ServiceError 404 si no existe."""
        with app.app_context():
            from app.services.auth_service import obtener_perfil

            with pytest.raises(ServiceError) as exc:
                obtener_perfil(9999)
            assert exc.value.status_code == 404


class TestListarUsuarios:
    """Pruebas para listar_usuarios() — líneas 116-129."""

    def test_listar_usuarios_vacio(self, app):
        """Debe retornar lista vacía si no hay usuarios."""
        with app.app_context():
            from app.services.auth_service import listar_usuarios

            resultado = listar_usuarios()
            assert isinstance(resultado, list)

    def test_listar_usuarios_con_datos(self, app, usuario_admin, usuario_recepcionista):
        """Debe retornar lista con usuarios."""
        with app.app_context():
            from app.services.auth_service import listar_usuarios

            resultado = listar_usuarios()
            assert len(resultado) >= 2

    def test_actualizar_usuario_exitoso(self, app, usuario_admin):
        """Debe actualizar nombre del usuario."""
        with app.app_context():
            from app.models.usuario import Usuario
            from app.services.auth_service import actualizar_usuario

            admin = Usuario.query.filter_by(email="admin@prueba.com").first()
            resultado = actualizar_usuario(admin.id, {"nombre": "Admin Actualizado"})
            assert resultado["nombre"] == "Admin Actualizado"

    def test_actualizar_usuario_inexistente(self, app):
        """Debe lanzar ServiceError 404 si no existe."""
        with app.app_context():
            from app.services.auth_service import actualizar_usuario

            with pytest.raises(ServiceError) as exc:
                actualizar_usuario(9999, {"nombre": "Test"})
            assert exc.value.status_code == 404
