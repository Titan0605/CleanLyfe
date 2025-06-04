from pymongo import MongoClient
from typing import Optional, Dict

mongo_client: Optional[MongoClient] = None

def init_db(app_mongo: MongoClient) -> None:
    """Initialize the database connection"""
    global mongo_client
    mongo_client = app_mongo
    
def get_client() -> MongoClient:
    if mongo_client is None:
        raise RuntimeError("Database not initialized. Call init_db first.")
    
    return mongo_client
    
def get_db(database_name: str = "worldmatters"):
    """Get a specific database from MongoDB client"""
    client = get_client()
    return client[database_name]

def get_collection(collection_name: str, database_name: str = "worldmatters"):
    """Get a specific collection from MongoDB"""
    db = get_db(database_name)
    return db[collection_name]