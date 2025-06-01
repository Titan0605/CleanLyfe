import os
from pymongo import MongoClient
from app.utils.db_utils import init_db
from app.database.db import init_app
from flask import Flask
from dotenv import load_dotenv
from app.routes import auth_routes, carbonfp_routes, carbonfp_view, index_view, home_view, hidricfp_view, hidricfp_routes, waterFlow_view, index_views

def create_app() -> Flask:
    load_dotenv()
    
    app = Flask(__name__)
    
    mongo_client: MongoClient = init_app(app)
    init_db(mongo_client)
    
    # env setup
    try:
        app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")
    except KeyError as e:
        print(e)
    
    # Blueprints registration views
    app.register_blueprint(index_view.bp)
    app.register_blueprint(home_view.bp)
    app.register_blueprint(carbonfp_view.bp)
    app.register_blueprint(hidricfp_view.bp)
    app.register_blueprint(waterFlow_view.bp)
    app.register_blueprint(index_views.bp)
    
    # Blueprint registration 
    app.register_blueprint(auth_routes.bp)
    app.register_blueprint(carbonfp_routes.bp)
    app.register_blueprint(hidricfp_routes.bp)
    
    return app

