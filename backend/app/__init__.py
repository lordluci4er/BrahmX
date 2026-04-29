from flask import Flask
from flask_cors import CORS
from .config.settings import get_config


def create_app():
    app = Flask(__name__)

    # -------- LOAD CONFIG --------
    config = get_config()
    app.config.from_object(config)

    # -------- CORS --------
    CORS(
        app,
        resources={r"/*": {"origins": app.config.get("CORS_ORIGINS", "*")}},
        supports_credentials=True
    )

    # -------- REGISTER BLUEPRINTS --------
    from .routes import main
    app.register_blueprint(main)

    # -------- HEALTH LOG --------
    print(f"✅ Flask app initialized ({config.__name__})")

    return app