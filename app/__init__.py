import os

from flask_mysqldb import MySQL
from app.utils.db_utils import init_db
from config import Config
from app.database.db import init_app
from flask import Flask
from dotenv import load_dotenv
from app.routes import auth_routes, carbonfp_routes, carbonfp_view, index_view, home_view

def create_app(config = Config) -> Flask:
    load_dotenv()
    
    app = Flask(__name__)
    
    app.config.from_object(config)
    
    mysql: MySQL = init_app(app)
    init_db(mysql)
    
    # env setup
    try:
        app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")
    except KeyError as e:
        print(e)
    
    # Blueprints registration views
    app.register_blueprint(index_view.bp)
    app.register_blueprint(home_view.bp)
    app.register_blueprint(carbonfp_view.bp)
    
    # Blueprint registration 
    app.register_blueprint(auth_routes.bp)
    app.register_blueprint(carbonfp_routes.bp)
    
    return app

