import os

class Config:
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:postgres@localhost/dbsgce'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get('YmlnZGF0YTIwMjU=') or 'YmlnZGF0YTIwMjU='
    FLASK_ENV = 'development'