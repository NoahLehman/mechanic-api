from flask import Flask
from config import Config
from extensions import db, limiter, cache

# import your blueprints after db is created to avoid circulars
from blueprints.customers.routes import customers_bp
from blueprints.mechanics.routes import mechanics_bp
from blueprints.service_tickets.routes import service_tickets_bp
from blueprints.inventory.routes import inventory_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    limiter.init_app(app)
    cache.init_app(app)

    app.register_blueprint(customers_bp, url_prefix="/customers")
    app.register_blueprint(mechanics_bp, url_prefix="/mechanics")
    app.register_blueprint(service_tickets_bp, url_prefix="/service_tickets")
    app.register_blueprint(inventory_bp, url_prefix="/inventory")

    return app
