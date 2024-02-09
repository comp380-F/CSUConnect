import os

database_uri = os.getenv('DATABASE_URL')

if database_uri and database_uri.startswith("postgres://"):
    database_uri = database_uri.replace("postgres://", "postgresql://", 1)

class Config:
    SECRET_KEY = 'my_secret_key'
    SQLALCHEMY_DATABASE_URI = database_uri
    SQLALCHEMY_TRACK_MODIFICATIONS = False