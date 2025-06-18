import os

class Config:
    SQLALCHEMY_DATABASE_URI = 'postgresql://sgce_database_user:zsdrqGq9lICjbszmxl9g3c8RB2s9jaMB@dpg-d19ff8re5dus738u4g5g-a.oregon-postgres.render.com/sgce_database'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get('YmlnZGF0YTIwMjU=') or 'YmlnZGF0YTIwMjU='
    FLASK_ENV = 'development'