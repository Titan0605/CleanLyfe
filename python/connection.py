""" 
pip install mysql-connector-python-rf

import mysql.connector 

connection = mysql.connector.connect(user="", password="", host="", port="", database="") --conexion a una base de datos

request = connection.cursor() --Permite consultar con querrys
request.execute("SELECT * FROM cat_jobs") --Aqui van los querrys

for name in request.fetchall(): --Recorre los resultados del querry
    print("Nombre del puesto", name)
    
connection.close() --cerramos la conexion a la base de datos

"""