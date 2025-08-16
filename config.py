import os

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "change-this-in-prod")
    JWT_ALGORITHM = "HS256"

    # Flask-Caching (swap to RedisCache in prod)
    CACHE_TYPE = os.environ.get("CACHE_TYPE", "SimpleCache")
    CACHE_DEFAULT_TIMEOUT = int(os.environ.get("CACHE_DEFAULT_TIMEOUT", "60"))

    # Flask-Limiter defaults (blanket protection)
    RATELIMIT_DEFAULT = os.environ.get("RATELIMIT_DEFAULT", "200 per hour")
    RATELIMIT_STORAGE_URI = os.environ.get("RATELIMIT_STORAGE_URI", "memory://")
