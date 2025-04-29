from flask_mysqldb import MySQL
import os

mysql = MySQL()

def init_app(app):
    # Basic configuration
    app.config['MYSQL_HOST'] = os.environ.get("DB_HOST")
    app.config['MYSQL_USER'] = os.environ.get("DB_USER")
    app.config['MYSQL_PASSWORD'] = os.environ.get("DB_PASSWORD")
    app.config['MYSQL_DB'] = os.environ.get("DB_NAME") 
    app.config['MYSQL_PORT'] = int(os.environ.get("DB_PORT"))
    
    mysql.init_app(app)
    app.mysql = mysql  
    
    return mysql