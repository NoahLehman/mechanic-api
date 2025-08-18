import os
from flask import Flask, current_app
from config import Config
from extensions import db, limiter, cache

# imports for your blueprints:
from blueprints.customers.routes import customers_bp
from blueprints.mechanics.routes import mechanics_bp
from blueprints.service_tickets.routes import service_tickets_bp
from blueprints.inventory.routes import inventory_bp

def create_app(config_class=Config, **config_overrides):
    # Ensure static folder points to app/static for Swagger file serving
    app = Flask(
        __name__,
        static_url_path="/static",
        static_folder=os.path.join(os.path.dirname(__file__), "static"),
    )

    # Base config
    app.config.from_object(config_class)
    # Apply overrides BEFORE init_app so extensions bind to correct settings
    if config_overrides:
        app.config.update(config_overrides)

    # Init extensions AFTER config is final
    db.init_app(app)
    cache.init_app(app)
    limiter.init_app(app)

    # Blueprints
    app.register_blueprint(customers_bp, url_prefix="/customers")
    app.register_blueprint(mechanics_bp, url_prefix="/mechanics")
    app.register_blueprint(service_tickets_bp, url_prefix="/service_tickets")
    app.register_blueprint(inventory_bp, url_prefix="/inventory")

    # Optional: per-blueprint rate limits
    limiter.limit(lambda: current_app.config.get("RATELIMIT_DEFAULT", "200 per hour"))(customers_bp)
    limiter.limit(lambda: current_app.config.get("RATELIMIT_DEFAULT", "200 per hour"))(mechanics_bp)
    limiter.limit(lambda: current_app.config.get("RATELIMIT_DEFAULT", "200 per hour"))(service_tickets_bp)
    limiter.limit(lambda: current_app.config.get("RATELIMIT_DEFAULT", "200 per hour"))(inventory_bp)

    return app
