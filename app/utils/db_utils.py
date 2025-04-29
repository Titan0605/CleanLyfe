from app.database.db import mysql
from flask_mysqldb import MySQLdb

# Function that returns the cursor 
def get_cursor():
    try:
        return mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    except KeyError as e:
        print(f"Error getting the cursor: {e}")
        raise

def get_commit():
    try:
        return  mysql.connection.commit()
    except KeyError as e:
        print(f"Error getting the commit: {e}")

# Function that returns the information from a db in json format
def get_table(table):
    try:
        cur = get_cursor()
        cur.execute(f"SELECT * FROM {table}")
        data = cur.fetchall()
        result = list(data)
        cur.close()
        return result
    except KeyError as e:
        print(f"{e}")