def create_db_conn(app):
    app.config['MYSQL_HOST'] = app.config["DB_HOST"]
    app.config['MYSQL_USER'] = app.config["DB_USER"]
    app.config['MYSQL_PASSWORD'] = app.config["DB_PASSWORD"]
    app.config['MYSQL_PORT'] = app.config["DB_PORT"]
    app.config['MYSQL_DB'] = app.config["DB_NAME"]    
    