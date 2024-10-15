from flask import Flask, render_template,request, redirect, url_for, flash 
from flask_mysqldb import MySQL

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(port= 5000, debug=True)
    
    app.config['MYSQL_HOST'] = 'localhost'
    app.config['MYSQL_USER'] = 'root'
    app.config['MYSQL_PASSWORD'] = ''
    app.config['MYSQL_DB'] = 'cleanlyfe'
    app.config['MYSQL_PORT'] = 3306
    mysql = MySQL(app)
    
    
@app.route('/login_fun', method = ['POST'])
def login_fun():
    if request.method == "POST":
        user_name = request.form['user_name']
        password = request.form["password"]
        confirmation = 3
        cur = mysql.connection.cursor()
        cur.execute('SELECT * TUsers')
        data = cur.fetchall()
        #for data_one in data: