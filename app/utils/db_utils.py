from flask_mysqldb import MySQLdb, MySQL
from typing import Optional, Any

mysql: Optional[MySQL] = None

def init_db(app_mysql: MySQL) -> None:
    """Initialize the database connection"""
    global mysql
    mysql = app_mysql

def get_mysql() -> MySQL:
    """Get the MySQL instance, raising an error if not initialized"""
    if mysql is None:
        raise RuntimeError("Database not initialized. Call init_db first.")
    return mysql

def get_cursor() -> Any:
    """Get a database cursor"""
    db: MySQL = get_mysql()
    if db.connection is None:
        raise RuntimeError("No database connection available")
    return db.connection.cursor(MySQLdb.cursors.DictCursor)

def get_commit() -> None:
    """Commit the current transaction"""
    db: MySQL = get_mysql()
    if db.connection is None:
        raise RuntimeError("No database connection available")
    db.connection.commit()

def get_table(table: str) -> list:
    """Get all rows from a table"""
    try:
        cur = get_cursor()
        cur.execute(f"SELECT * FROM {table}")
        data = cur.fetchall()
        result = list(data)
        cur.close()
        return result
    except Exception as e:
        print(f"Error getting table data: {e}")
        raise