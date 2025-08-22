from app import create_app
from flask_swagger_ui import get_swaggerui_blueprint

app = create_app()

# Swagger UI setup
SWAGGER_URL = '/docs'
API_URL = '/static/swagger.yaml'
swaggerui_bp = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={'app_name': "Mechanic Service API"},
    blueprint_name="swagger_ui_mechanic"
)
app.register_blueprint(swaggerui_bp, url_prefix=SWAGGER_URL)