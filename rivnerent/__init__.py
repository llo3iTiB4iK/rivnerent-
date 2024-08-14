from flask import Flask
from .models import User
from .extensions import bootstrap, db, login_manager, csrf, sheetdb
from .main import main_bp
from .auth import auth_bp
from .admin import admin_bp


def create_app(config_file="config.py"):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_pyfile(config_file)

    # Ініціалізація розширень
    bootstrap.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)
    sheetdb.init_app(app)

    # Ініціалізація користувачів
    users = {app.config['ADMIN_LOGIN']: {'password': app.config['ADMIN_PASSWORD']}}

    @login_manager.user_loader
    def load_user(user_id):
        if user_id in users:
            return User(user_id)
        return None

    # Ін'єкція змінної ADMIN_PHONE в контекст шаблонів
    @app.context_processor
    def inject_admin_phone():
        return {'ADMIN_PHONE_NUM': app.config['ADMIN_PHONE']}

    # Реєстрація модулів у основній програмі
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)

    # Створення БД (якщо не існує)
    with app.app_context():
        db.create_all()

    return app
