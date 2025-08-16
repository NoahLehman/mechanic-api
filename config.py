class Config:
    SECRET_KEY = "dev-secret"
    SQLALCHEMY_DATABASE_URI = "sqlite:///mechanic.db"   # local file DB
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # caching
    CACHE_TYPE = "SimpleCache"
    CACHE_DEFAULT_TIMEOUT = 60

    # rate limiting
    RATELIMIT_DEFAULT = "200 per hour"
    RATELIMIT_STORAGE_URI = "memory://"
