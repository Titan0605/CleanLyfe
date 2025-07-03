import os
from pymongo import MongoClient
from app.utils.db_utils import init_db
from app.database.db import init_app
from flask import Flask
from dotenv import load_dotenv
# from app.routes import auth_routes, carbonfp_routes, carbonfp_view, index_view, home_view, hidricfp_view, hidricfp_routes, waterFlow_view, index_views
from app.routes import indexes_views, auth_views, auth_routes, home_view, hydricfp_routes, hydricfp_view, carbonfp_view, waterflow_views, waterflow_routes, carbonfp_routes

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
    app.register_blueprint(indexes_views.bp)
    app.register_blueprint(auth_views.bp)
    app.register_blueprint(home_view.bp)
    app.register_blueprint(carbonfp_view.bp)
    app.register_blueprint(hydricfp_view.bp)
    app.register_blueprint(waterflow_views.bp)
    app.register_blueprint(waterflow_routes.bp)
    
    # # Blueprint registration 
    app.register_blueprint(auth_routes.bp)
    app.register_blueprint(carbonfp_routes.bp)
    app.register_blueprint(hydricfp_routes.bp)
    
    return app

