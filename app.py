from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL

#este es para declarar una varianble tipo flask (es obligatorio)
app = Flask(__name__)

#This a security step for the flash messages
app.secret_key = 'mysecretkey'
#Configuracion necesaria para hacer una conexion a la base de datos
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'cleanlyfe'
app.config['MYSQL_PORT'] = 3306
mysql = MySQL(app)

app.secret_key = 'mysecretkey'

#el app route con el / es para que sea la primera pagina en aparecer
@app.route('/')
def index():
    return render_template('index.html')

#Esto es lo que se va a ejecutar cuando el formulario de login haga el submit, forzosamente es con el metodo POST
@app.route('/login_fun', methods=['POST'])
def login_fun():
    #Tenemos que verificar que el metodo requerido es POST para evitar errores
    if request.method == "POST":
        #Creamos las variables necesarias para verificar el inicio de sesion, el valor se trae desde name del HTML
        user_name = request.form['user_name']
        password = request.form["password"]
        user_id = 2
        #Esta variable es para confirmar si el password y el user name son iguales a los de la base de datos
        confirmation = 3
        #Creamos un cursor, que es como un traductor/comunicador entre el backend y la base de datos
        cur = mysql.connection.cursor()
        #Con el comando execute pides que quieres hacer (CRUD o lo que quieras)
        cur.execute('SELECT * FROM tusers')
        #El fecthall se hace en los selects para traer todos los datos, se va a traer una lista dentro de otra lista con todos los datos
        data = cur.fetchall()
        #Este for es para recorrer todas las listas puestas y verificar
        for login in data:
            #Si los datos son iguales entonces confirmation se va a cambiar a uno
            if login[4] == user_name and login[6] == password:
                confirmation = 1
                user_id = login[0]
                break
        #Si el confirmation es 1 se va a mandar a la funcion de go_main_page que va a renderizar el html cleanlyfe, si es diferente de 1 entonces va a renderizar la misma pagina
        if confirmation == 1:
            #El flash es un mensaje que se va a mandar a los html por medio de jinja2
            flash('You have been logged in')
            return redirect(url_for('go_cleanlyfe', id = user_id))
        else:
            flash('The data was wrong')
            return redirect(url_for('go_login'))

@app.route('/redirect_reg', methods=['GET'])
def redirect_reg():
    if request.method == 'GET':
        return redirect(url_for('go_register'))

@app.route('/register_fun', methods=['POST'])
def register_fun():
    if request.method == 'POST':
        email = request.form['email']
        user_name = request.form['usuario']
        password = request.form['password']
        con_password = request.form['con_password']
        first_name = request.form['first_name']
        last_name = request.form['last_name']

        if password == con_password:
            cur = mysql.connection.cursor()
            cur.execute('INSERT INTO tusers (id_type_member, first_name, last_name, user_name, user_email, user_password, active, created_at) VALUES (1, %s, %s, %s, %s, %s, 1, NOW())', (first_name, last_name, user_name, email, password))
            mysql.connection.commit()
            flash('You have been registered')
            return redirect(url_for('go_login'))
        else:
            flash('The confirm password was not the same')
            return redirect(url_for('go_register'))



#Esta ruta es para renderizar la pagina de login (el metodo get se obtiene cuando es redireccionado con redirect(url_for()))
@app.route('/go_login', methods=['GET','POST'])
def go_login():
    if request.method == 'POST' or request.method == 'GET':
        return render_template('login.html')

#This route is for opening and renderising the register
@app.route('/go_register', methods=['GET','POST'])
def go_register():
    if request.method=='POST' or request.method=='GET':
        return render_template('register.html')

#This route is for opening the user's profile
@app.route('/go_user_profile', methods=['GET', 'POST'])
def go_user_profile():
    if request.method == 'POST' or request.method == 'GET':
        return render_template('userProfile.html')   
    
#Esta ruta es para renderizar la main page
@app.route('/go_main_page', methods=['GET', 'POST'])
def go_main_page():
    if request.method == 'GET' or request.method == "POST":
        return render_template('index.html')

#This route is for opening and renderising the cleanlyfe page
@app.route('/go_cleanlyfe/<id>', methods=['GET', 'POST'])
def go_cleanlyfe(id):
    if request.method == 'POST' or request.method == 'GET':
        id = int(id)
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM tusers WHERE id_user = %s', (id,))
        data = cur.fetchall()
        return render_template('cleanlyfe.html', user = data[0])

#This route is for opening and renderising the missions page
@app.route('/go_missions/<id>', methods=['GET', 'POST'])
def go_missions(id):
    if request.method == 'POST' or request.method == 'GET':
        id = int(id)
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM tusers WHERE id_user = %s', (id,))
        data = cur.fetchall()
        return render_template('misions.html', user = data[0])

#This route is for opening and renderising the missions page
@app.route('/go_index', methods=['GET', 'POST'])
def go_index():
    if request.method == 'POST' or request.method == 'GET':
        return render_template('index.html')

#This is a method that recieves an error and renderising the error handle page
def page_not_found(error):
    return render_template("404.html"), 404

#Esto es para que corra la pagina como un servidor
if __name__ == "__main__":
    #This prevents that appears an error of page not found and shows a error handle page
    app.register_error_handler(404, page_not_found)
    app.run(port= 5000, debug=True)