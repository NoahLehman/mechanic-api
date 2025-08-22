import os

class Config:
    SECRET_KEY = "super-secret"   # change in production
    JWT_ALGORITHM = "HS256"       #

    # Database
    SQLALCHEMY_DATABASE_URI = "sqlite:///mechanic.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Flask-Caching
    CACHE_TYPE = "SimpleCache"
    CACHE_DEFAULT_TIMEOUT = 60

    # Flask-Limiter
    RATELIMIT_DEFAULT = "200 per hour"
    RATELIMIT_STORAGE_URI = "memory://"

class ProductionConfig:
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLSQLALCHEMY_DATABASE_URI')
    CACHE_TYPE = "SimpleCache"
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'super-secret'
