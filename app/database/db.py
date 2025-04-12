from flask_mysqldb import MySQL

mysql = MySQL()

# Database connection setup
def init_app(app):
    mysql.init_app(app)