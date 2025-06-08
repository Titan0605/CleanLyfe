from pymongo import MongoClient
from dotenv import load_dotenv
import os


def init_app(app) -> MongoClient:
    load_dotenv()
    
    MONGO_USER = os.environ.get("DB_USER")
    MONGO_PASSWORD = os.environ.get("DB_PASSWORD")
    MONGO_CONNECTION_TYPE = os.environ.get("DB_CONNECTION")
    
    match MONGO_CONNECTION_TYPE:
        case "local":
            URI = "mongodb://localhost:27017/"
        case "cloud":
            URI = f"mongodb+srv://{MONGO_USER}:{MONGO_PASSWORD}@cleanlyfe.1ucxqaz.mongodb.net/?retryWrites=true&w=majority&appName=cleanlyfe"
            
    mongo_client = MongoClient(URI) 
    app.config["MONGO_CLIENT"] = mongo_client
    
    return mongo_client