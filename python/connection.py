""" pip install mysql-connector-python """

import mysql.connector 

connection = mysql.connector.connect(user="root", password="", host="localhost", port="3306", database="class_cafebis") #conexion a una base de datos

request = connection.cursor() #Permite consultar con querrys
request.execute("SELECT * FROM cat_jobs")   #--Aqui van los querrys

for name in request.fetchall():
    print("Nombre del puesto", name) #Recorre los resultados del querry

connection.close() #Cerramos la conexion a la base de datos