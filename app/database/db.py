from flask_mysqldb import MySQL
import os

mysql = MySQL()

def init_app(app) -> MySQL:
    """
    Function to create the connection to the Database

    Args:
        app (_type_): Receive an object app from Flask

    Returns:
        MySQL: Returns a Mysql object with access credentials
    """

    #TESTING WITH DB FOR DEVELOP THE DESIGN
    app.config['MYSQL_HOST'] = os.environ.get("DB_HOST")
    app.config['MYSQL_USER'] = os.environ.get("DB_USER")
    app.config['MYSQL_PASSWORD'] = os.environ.get("DB_PASSWORD")
    app.config['MYSQL_DB'] = os.environ.get("DB_NAME") 
    app.config['MYSQL_PORT'] = int(os.environ.get("DB_PORT"))
    
    mysql.init_app(app)
    app.mysql = mysql  
    
    return mysql