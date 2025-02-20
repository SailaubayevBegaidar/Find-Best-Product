from flask import Flask
from flask_pymongo import PyMongo
from flask_jwt_extended import JWTManager
from config import config
import logging
from logging.handlers import RotatingFileHandler
import os

# Initialize extensions
mongo = PyMongo()
jwt = JWTManager()

def create_app(config_name='default'):
    """Application factory function to create and configure the Flask app."""
    
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(config[config_name])
    
    # Initialize extensions with app
    mongo.init_app(app)
    jwt.init_app(app)
    
    # Configure logging
    if not app.debug:
        if not os.path.exists('logs'):
            os.mkdir('logs')
        file_handler = RotatingFileHandler(
            'logs/findbestproduct.log', 
            maxBytes=10240, 
            backupCount=10
        )
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
        ))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)
        app.logger.setLevel(logging.INFO)
        app.logger.info('FindBestProduct startup')
    
    # Register blueprints
    with app.app_context():
        from app.routes import bp as routes_bp
        from app.auth import auth_bp
        app.register_blueprint(routes_bp)
        app.register_blueprint(auth_bp)
    
    return app
