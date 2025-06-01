from pymongo import MongoClient
import os


def init_app(app) -> MongoClient:
    # """
    # Function to create the connection to the Database

    # Args:
    #     app (_type_): Receive an object app from Flask

    # Returns:
    #     MySQL: Returns a Mysql object with access credentials
    # """
    # app.config['MYSQL_HOST'] = os.environ.get("DB_HOST")
    # app.config['MYSQL_USER'] = os.environ.get("DB_USER")
    # app.config['MYSQL_PASSWORD'] = os.environ.get("DB_PASSWORD")
    # app.config['MYSQL_DB'] = os.environ.get("DB_NAME") 
    # app.config['MYSQL_PORT'] = int(os.environ.get("DB_PORT", default=3306))
    
    # mysql.init_app(app)
    # app.mysql = mysql
    
    MONGO_USER = os.environ.get("DB_USER")
    MONGO_PASSWORD = os.environ.get("DB_PASSWORD")
    MONGO_CONNECTION_TYPE = os.environ.get("DB_CONNECTION")
    
    match MONGO_CONNECTION_TYPE:
        case "local":
            URI = "mongodb://localhost:27017/"
        case "cloud":
            URI = f"mongodb+srv://{MONGO_USER}:{MONGO_PASSWORD}@cleanlyfe.1ucxqaz.mongodb.net/?retryWrites=true&w=majority&appName=cleanlyfe"
            
    mongo_client = MongoClient(URI) 
    app.mongo_client = mongo_client
    
    return mongo_client