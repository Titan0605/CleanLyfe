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
    
def get_db(database_name: str = "cleanlyfe"):
    """Get a specific database from MongoDB client"""
    client = get_client()
    return client[database_name]

def get_collection(collection_name: str, database_name: str = "cleanlyfe"):
    """Get a specific collection from MongoDB"""
    db = get_db(database_name)
    return db[collection_name]

# def get_mysql() -> MySQL:
#     """Get the MySQL instance, raising an error if not initialized"""
#     if mysql is None:
#         raise RuntimeError("Database not initialized. Call init_db first.")
#     return mysql

# def get_cursor() -> Any:
#     """Get a database cursor"""
#     db: MySQL = get_mysql()
#     if db.connection is None:
#         raise RuntimeError("No database connection available")
#     return db.connection.cursor(MySQLdb.cursors.DictCursor)

# def exec_commit() -> None:
#     """Commit the current transaction"""
#     db: MySQL = get_mysql()
#     if db.connection is None:
#         raise RuntimeError("No database connection available")
#     db.connection.commit()

# def get_table(table: str) -> list:
#     """Get all rows from a table"""
#     try:
#         cur = get_cursor()
#         cur.execute(f"SELECT * FROM {table}")
#         data = cur.fetchall()
#         result = list(data)
#         cur.close()
#         return result
#     except Exception as e:
#         print(f"Error getting table data: {e}")
#         raise