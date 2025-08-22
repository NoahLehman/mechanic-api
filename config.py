import os

class Config:
    SECRET_KEY = "super-secret"   # change in production
    JWT_ALGORITHM = "HS256"       #

    # Database
    SQLALCHEMY_DATABASE_URI = "postgresql://noahl:BlAqrYBUZQDtA60UoJ6QrKYFgxk4iCDJ@dpg-d2jrihf5r7bs73e37jc0-a.oregon-postgres.render.com/database_uyqs"
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
    JWT_ALGORITHM = "HS256"
    CACHE_DEFAULT_TIMEOUT = 60

    # Flask-Limiter
    RATELIMIT_DEFAULT = "200 per hour"
    RATELIMIT_STORAGE_URI = "memory://"