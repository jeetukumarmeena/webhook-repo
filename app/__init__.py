from flask import Flask
from flask_cors import CORS
from app.extensions import mongo
from app.routes import webhook_bp, ui_bp

def create_app():
    app = Flask(__name__)
    
    # Enable CORS for all routes
    CORS(app)
    
    # Load configuration
    app.config['MONGODB_URI'] = 'mongodb://localhost:27017/'
    app.config['DATABASE_NAME'] = 'github_webhooks'
    app.config['COLLECTION_NAME'] = 'events'
    
    # Initialize extensions
    mongo.init_app(app)
    
    # Register blueprints
    app.register_blueprint(webhook_bp)
    app.register_blueprint(ui_bp)
    
    return app