import os
from config import Config
from app.database.db import init_app
from flask import Flask
from dotenv import load_dotenv
from app.routes import index_view, home_view
from app.services import index_service, home_service

def create_app(config = Config):
    load_dotenv()
    
    app = Flask(__name__)
    
    app.config.from_object(config)
    
    init_app(app)    
    
    # env setup
    try:
        app.config["DB_HOST"] = os.environ.get("DB_HOST")
        app.config["DB_USER"] = os.environ.get("DB_USER")
        app.config["DB_PASSWORD"] = os.environ.get("DB_PASSWORD")
        app.config["DB_PORT"] = os.environ.get("DB_PORT")
        app.config["DB_NAME"] = os.environ.get("DB_NAME")   
        app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")
    except KeyError as e:
        print(e)
    
    # Blueprints registration
    app.register_blueprint(index_view.bp)
    app.register_blueprint(index_service.bp)
    app.register_blueprint(home_view.bp)
    return app

