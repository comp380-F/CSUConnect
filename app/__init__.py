import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from flask_login import LoginManager
from flask_migrate import Migrate

from config import Config

metadata = MetaData(
    naming_convention={
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
    }
)

db = SQLAlchemy(metadata=metadata)
login_manager = LoginManager()
login_manager.login_view = '/login' # Specifying the login view


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize the db and migrate
    db.init_app(app)
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

    from .club import club_bp
    app.register_blueprint(club_bp)

    return app



    