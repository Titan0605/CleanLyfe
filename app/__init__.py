import os
from config import Config
from app.database.db import init_app
from flask import Flask
from dotenv import load_dotenv
from app.routes import index_view, home_view, auth

def create_app(config = Config):
    load_dotenv()
    
    app = Flask(__name__)
    
    app.config.from_object(config)
    
    mysql = init_app(app)    
    
    # env setup
    try:
        app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")
    except KeyError as e:
        print(e)
    
    # Blueprints registration
    app.register_blueprint(index_view.bp)
    app.register_blueprint(auth.bp)
    app.register_blueprint(home_view.bp)
    
    return app

