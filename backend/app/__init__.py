"""Application Factory — creación e inicialización de la app Flask."""
from flask import Flask, jsonify
from flask_cors import CORS
from config import config
from app.extensions import db, es_token_blocklist, jwt, ma


def create_app(config_name: str = "development") -> Flask:
    """Crea y configura la aplicación Flask según el entorno indicado."""
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    # Inicializar extensiones
    db.init_app(app)
    jwt.init_app(app)
    ma.init_app(app)

    # Configurar CORS con orígenes del entorno
    origins = app.config.get("CORS_ORIGINS", "")
    CORS(app, origins=[o.strip() for o in origins.split(",") if o.strip()])

    # Callbacks JWT
    _registrar_callbacks_jwt(app)

    # Registrar blueprints
    from app.routes.auth_routes import bp as auth_bp
    from app.routes.usuarios_routes import bp as usuarios_bp
    from app.routes.mesas_routes import bp as mesas_bp
    from app.routes.reservas_routes import bp as reservas_bp
    from app.routes.carta_routes import bp as carta_bp
    from app.routes.takeaway_routes import bp as takeaway_bp
    from app.routes.admin_routes import bp as admin_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(usuarios_bp)
    app.register_blueprint(mesas_bp)
    app.register_blueprint(reservas_bp)
    app.register_blueprint(carta_bp)
    app.register_blueprint(takeaway_bp)
    app.register_blueprint(admin_bp)

    # Manejadores globales de errores JWT
    _registrar_manejadores_errores(app)

    @app.route("/api/health")
    def health():
        """Endpoint de salud para verificar que la API está activa."""
        return jsonify({"status": "ok", "message": "API Pollería Leña y Carbón"})

    return app


def _registrar_callbacks_jwt(app: Flask) -> None:
    """Registra callbacks de Flask-JWT-Extended."""

    @jwt.token_in_blocklist_loader
    def verificar_token_blocklist(_jwt_header, jwt_payload):
        return es_token_blocklist(jwt_payload["jti"])

    @jwt.expired_token_loader
    def token_expirado(_jwt_header, _jwt_payload):
        return jsonify({"error": "Token expirado. Inicie sesión nuevamente."}), 401

    @jwt.invalid_token_loader
    def token_invalido(error):
        return jsonify({"error": f"Token inválido: {error}"}), 401

    @jwt.unauthorized_loader
    def sin_autorizacion(error):
        return jsonify({"error": f"Se requiere autenticación: {error}"}), 401


def _registrar_manejadores_errores(app: Flask) -> None:
    """Registra manejadores de excepciones HTTP globales."""

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({"error": str(error.description) if error.description else "Solicitud inválida"}), 400

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({"error": str(error.description) if error.description else "Recurso no encontrado"}), 404

    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({"error": "Método HTTP no permitido"}), 405

    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return jsonify({"error": "Error interno del servidor"}), 500
