import os

database_uri = os.getenv('DATABASE_URL')

if uri and uri.startswith("postgres://"):
    uri = uri.replace("postgres://", "postgresql://", 1)

class Config:
    SECRET_KEY = 'my_secret_key'
    SQLALCHEMY_DATABASE_URI = database_uri or 'sqlite:///app.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False