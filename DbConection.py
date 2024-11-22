import pymysql

def conection():
    connection = pymysql.connect(
            host="localhost",
            user="root",
            password="",
            database="testdictionary"
        )
    return connection
def get_dict_cursor():
    connection = conection()
    return connection.cursor(pymysql.cursors.DictCursor)