from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from .config import Config


db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    CORS(app, resources={
        r"/api/*": {
            "origins": "*",  # For dev, restrict in production later
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Authorization", "Content-Type"]
        }
    })
    db.init_app(app)

    from .routes import product_bp
    app.register_blueprint(product_bp, url_prefix="/api/products")

    with app.app_context():
        db.create_all()

    return app
