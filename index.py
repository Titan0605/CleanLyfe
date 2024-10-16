from flask import Flask, render_template,request, redirect, url_for, flash 
from flask_mysqldb import MySQL
#este es para declarar una varianble tipo flask (es obligatorio)
app = Flask(__name__)

#el app route con el / es para que sea la primera pagina en aparecer 
@app.route('/')
def index():
    return render_template('cleanlyfe.html')

#Esto es para que corra la pagina como un servidor
if __name__ == "__main__":
    app.run(port= 5000, debug=True)
    
#Configuracion necesaria para hacer una conexion a la base de datos
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'cleanlyfe'
app.config['MYSQL_PORT'] = 3306
mysql = MySQL(app)
    
#Esto es lo que se va a ejecutar cuando el formulario de login haga el submit, forzosamente es con el metodo POST
@app.route('/login_fun', method = ['POST'])
def login_fun():
    #Tenemos que verificar que el metodo requerido es POST para evitar errores
    if request.method == "POST":
        #Creamos las variables necesarias para verificar el inicio de sesion, el valor se trae desde name del HTML 
        user_name = request.form['user_name']
        password = request.form["password"]
        #Esta variable es para confirmar si el password y el user name son iguales a los de la base de datos
        confirmation = 3
        #Creamos un cursor, que es como un traductor/comunicador entre el backend y la base de datos
        cur = mysql.connection.cursor()
        #Con el comando execute pides que quieres hacer (CRUD o lo que quieras)
        cur.execute('SELECT * TUsers')
        #El fecthall se hace en los selects para traer todos los datos, se va a traer una lista dentro de otra lista con todos los datos
        data = cur.fetchall()
        #Este for es para recorrer todas las listas puestas y verificar
        for login in data:
            #Si los datos son iguales entonces confirmation se va a cambiar a uno
            if login[4] == user_name and login[6] == password:
                confirmation = 1
                break
        #Si el confirmation es 1 se va a mandar a la funcion de go_main_page que va a renderizar el html cleanlyfe, si es diferente de 1 entonces va a renderizar la misma pagina     
        if confirmation == 1:
            #El flash es un mensaje que se va a mandar a los html por medio de jinja2
            flash('You have been logged in')
            return redirect(url_for('go_main_page'))
        else:
            flash('The data was wrong')
            return redirect(url_for('go_login'))
        
#Esta ruta es para renderizar la pagina de login (el metodo get se obtiene cuando es redireccionado con redirect(url_for()))
@app.route('/go_login', methods=['GET','POST'])
def go_login():
    if request.method == 'POST' or request.method == 'GET':
        return render_template('login.html')
    
#Esta ruta es para renderizar la main page 
@app.route('/go_main_page', methods=['GET', 'POST'])
def go_main_page():
    if request.method == 'GET' or request.method == "POST":
        return render_template('index.html')