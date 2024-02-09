import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

from config import Config

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = '/login' # Specifying the login view


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    login_manager.init_app(app)

    from app.models import User

    # User loader func
    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get((User), int(user_id))

    from .routes import bp as routes_bp
    app.register_blueprint(routes_bp)

    return app



    