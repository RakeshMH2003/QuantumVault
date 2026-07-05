import os
from flask import Flask
from models.models import db
from utils.authentication import login_manager, bcrypt
from routes.auth import auth_bp
from routes.dashboard import dashboard_bp
from routes.crypto import crypto_bp
from routes.admin import admin_bp

def create_app():
    app = Flask(__name__)

    # ── Security ─────────────────────────────────────────────────────────────
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'quantumvault-ultra-secret-key-2026-qrc')

    # ── PostgreSQL ────────────────────────────────────────────────────────────
    PG_USER = os.environ.get('PG_USER', 'qrc_user')
    PG_PASS = os.environ.get('PG_PASS', 'qrc_admin_2026')
    PG_HOST = os.environ.get('PG_HOST', 'localhost')
    PG_PORT = os.environ.get('PG_PORT', '5432')
    PG_DB   = os.environ.get('PG_DB',   'qrc_vault')

    app.config['SQLALCHEMY_DATABASE_URI'] = (
        f'postgresql+psycopg2://{PG_USER}:{PG_PASS}@{PG_HOST}:{PG_PORT}/{PG_DB}'
    )
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
        'pool_pre_ping': True,
        'pool_recycle': 300,
    }
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50 MB

    # ── Extensions ────────────────────────────────────────────────────────────
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view             = 'auth.login'
    login_manager.login_message          = 'Please log in to access QuantumVault.'
    login_manager.login_message_category = 'info'

    # ── Blueprints ────────────────────────────────────────────────────────────
    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(crypto_bp)
    app.register_blueprint(admin_bp)

    # ── Create tables + seed admin ───────────────────────────────────────────
    with app.app_context():
        db.create_all()
        _seed_admin(app)

    return app


def _seed_admin(app):
    """Create default admin account if it does not exist."""
    from models.models import User
    from utils.authentication import bcrypt as _bc
    if not User.query.filter_by(username='admin').first():
        admin = User(
            username      = 'admin',
            email         = 'admin@quantumvault.io',
            password_hash = _bc.generate_password_hash('Admin@2026').decode('utf-8'),
            role          = 'admin',
            company       = 'QuantumVault HQ',
        )
        db.session.add(admin)
        db.session.commit()
        print('[QuantumVault] Default admin created: admin / Admin@2026')


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=5000)
