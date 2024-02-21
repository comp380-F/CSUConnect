import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate

# Import the config class
from config import Config

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = '/login' # Specifying the login view


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize the db
    db.init_app(app)

    # Initialize the db migration
    migrate = Migrate(app, db)

    # Initialize the login manager
    login_manager.init_app(app)

    # Import the models
    from app.models import User

    # User loader func
    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get((User), int(user_id))

    # Register the blueprints
    from .routes import bp as routes_bp
    app.register_blueprint(routes_bp)

    from .auth import auth_bp
    app.register_blueprint(auth_bp)

    from .user import user_bp
    app.register_blueprint(user_bp)

    from .event import event_bp
    app.register_blueprint(event_bp)

    return app



    