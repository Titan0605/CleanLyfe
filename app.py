from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_mysqldb import MySQL
import water_products_calculus
import transportCalculus, DbConection
import pymysql
import carbon_products_calculus
from werkzeug.utils import secure_filename 

from random import sample

import os

from random import random

#este es para declarar una varianble tipo flask (es obligatorio)
app = Flask(__name__)

#This a security step for the flash messages
app.secret_key = 'mysecretkey'
#Configuracion necesaria para hacer una conexion a la base de datos
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'cleanlyfe'
#YOU MUST CHANGE THE PORT IF ANOTHER PERSON WERE EDITING THE CODE (You have to put your own port of your xampp)
app.config['MYSQL_PORT'] = 3306
mysql = MySQL(app)

app.jinja_env.globals.update(random=random)

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
        #Creamos un cursor, que es como un traductor/comunicador entre el backend y la base de datos
        cur = mysql.connection.cursor()
        #Con el comando execute pides que quieres hacer (CRUD o lo que quieras)
        cur.execute('SELECT * FROM tusers WHERE user_name = %s AND user_password = %s', (user_name, password))
        #El fecthall se hace en los selects para traer todos los datos, se va a traer una lista dentro de otra lista con todos los datos
        data = cur.fetchone()

        #Si el confirmation es 1 se va a mandar a la funcion de go_main_page que va a renderizar el html cleanlyfe, si es diferente de 1 entonces va a renderizar la misma pagina
        if data:

            session['user']=user_name
            session['password']=password
            session['first_name']= data[2]
            session['last_name']= data[3]
            session['email']= data[5]
            session['id']= data[0]
            session['img'] = data[7]
            #El flash es un mensaje que se va a mandar a los html por medio de jinja2
            flash('You have been logged in')
            return redirect(url_for('go_cleanlyfe'))
        else:
            flash('The data was wrong')
            return redirect(url_for('go_login'))

@app.route('/redirect_reg', methods=['GET'])
def redirect_reg():
    if request.method == 'GET':
        return redirect(url_for('go_register'))

@app.route('/logout', methods=['GET'])
def logout():
    if 'user' in session:
        session.pop('user', None)
        session.pop('password', None)
        session.pop('first_name', None)
        session.pop('last_name', None)
        session.pop('email', None)
        session.pop('id', None)
        session.pop('img', None)
        return render_template('index.html')
    return render_template('index.html')

@app.route('/register_fun', methods=['POST'])
def register_fun():
    if request.method == 'POST':
        encrypt_pass = 'ewte700et74j'
        email = request.form['email']
        user_name = request.form['username']
        password = request.form['password']
        con_password = request.form['confirm-password']

        cur = mysql.connection.cursor()

        cur.execute('SELECT * FROM tusers')
        data = cur.fetchall()

        for user in data:
            if user[4] == user_name:
                flash('That user has already been taken')
                return redirect(url_for('go_register'))

        if len(password) >= 8:
            if password == con_password:
                cur.execute('INSERT INTO tusers (id_type_member, user_name, user_mail, user_password, active, created_at) VALUES (1, %s, aes_encrypt(%s, %s), SHA(%s), 1, NOW())', (user_name, email, encrypt_pass, password))
                mysql.connection.commit()
                flash('You have been registered')
                return redirect(url_for('go_login'))
            else:
                flash('The confirm password was not the same')
                return redirect(url_for('go_register'))
        else:
            flash('The length of the password can not be less than 8 characters')
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
        if 'id' in session:
            user_id = session['id']
            user_name = session['user']
            photo = session['img']
            cur = mysql.connection.cursor()
            cur.execute('SELECT * FROM tusers WHERE id_user = %s', (user_id,))
            data = cur.fetchone()
            print(data)
            return render_template('userProfile.html', user_data = data, user = user_name, photo = photo)

#Esta ruta es para renderizar la main page
@app.route('/go_main_page', methods=['GET', 'POST'])
def go_main_page():
    if request.method == 'GET' or request.method == "POST":
        return render_template('index.html')

#This route is for opening and renderising the cleanlyfe page
@app.route('/go_cleanlyfe', methods=['GET', 'POST'])
def go_cleanlyfe():
    if request.method == 'POST' or request.method == 'GET':

        if not 'user' in session:
            flash('You have not logged in yet')
            return render_template('404.html')

        user = session['user']
        id_user = session['id']
        
        if user == 'invited':
            return render_template('404.html')
        else:
            history_url = f'http://localhost:3000/d-solo/ae5crwj1cuadce/cleanlyfe-dashboards?from=1732812935134&to=1732834535135&timezone=browser&var-idUser={id_user}&orgId=1&panelId=3&__feature.dashboardSceneSolo'
            last_carbon = f'http://localhost:3000/d-solo/ae5crwj1cuadce/cleanlyfe-dashboards?from=1732812935134&to=1732834535135&timezone=browser&var-idUser={id_user}&orgId=1&panelId=1&__feature.dashboardSceneSolo'
            last_hidric = f'http://localhost:3000/d-solo/ae5crwj1cuadce/cleanlyfe-dashboards?from=1732812935134&to=1732834535135&timezone=browser&var-idUser={id_user}&orgId=1&panelId=2&__feature.dashboardSceneSolo'
            carbon_section = f'http://localhost:3000/d-solo/ae5crwj1cuadce/cleanlyfe-dashboards?from=1733132785556&to=1733154385556&timezone=browser&var-idUser={id_user}&orgId=1&panelId=4&__feature.dashboardSceneSolo'
            carbon_footprints = f'http://localhost:3000/d-solo/ae5crwj1cuadce/cleanlyfe-dashboards?from=1732835486670&to=1732857086670&timezone=browser&var-idUser={id_user}&showCategory=Standard%20options&orgId=1&panelId=6&__feature.dashboardSceneSolo'
            hidric_section = f'http://localhost:3000/d-solo/ae5crwj1cuadce/cleanlyfe-dashboards?from=1732835486670&to=1732857086670&timezone=browser&var-idUser={id_user}&orgId=1&panelId=7&__feature.dashboardSceneSolo'
            hidric_footprints = f'http://localhost:3000/d-solo/ae5crwj1cuadce/cleanlyfe-dashboards?from=1732835486670&to=1732857086670&timezone=browser&var-idUser={id_user}&orgId=1&panelId=5&__feature.dashboardSceneSolo'
            
            photo = session['img']
            
            return render_template('cleanlyfe.html', user = user, grafana_user_history = history_url, grafana_user_last_carbon = last_carbon, grafana_user_last_hidric = last_hidric, grafana_carbon_section = carbon_section, grafana_carbon_footprints = carbon_footprints, grafana_hidric_section = hidric_section, grafana_hidric_footprints = hidric_footprints, photo = photo)


#This route is for opening and renderising the missions page
@app.route('/go_missions', methods=['GET', 'POST'])
def go_missions():
    if request.method == 'POST' or request.method == 'GET':

        if 'id' in session:
            id_user = session['id']
            if id_user == 10:
                return 'You have not logged in yet'
            else:
                user_name =session['user']
                photo = session['img']
                return render_template('misions.html', user = user_name, photo = photo)
        return "You have not logged in yet"

#This route is for opening and renderising the missions page
@app.route('/go_index', methods=['GET', 'POST'])
def go_index():
    if request.method == 'POST' or request.method == 'GET':
        return render_template('index.html')

@app.route('/go_hidric_cal', methods=['GET'])
def go_hidric_cal():
    if request.method == 'GET':
        if 'id' in session:
            user_name = session['user']
            user_id = session['id']
            photo = session['img']
            if not photo:
                photo = ''
            
        else:
            session['id']= int(10)
            session['user']='invited'
            user_id = session['id']
            user_name = session['user']
            photo = ''

        if user_id != 10:
            cur = mysql.connection.cursor()
            cur.execute('SELECT hidric_page FROM tuser_log WHERE id_user = %s', (user_id,))
            data = cur.fetchone()
            page = data[0]
            if page == 1:
                return render_template('cal_hid.html', user = user_name, id = user_id, photo = photo)
            elif page == 2:
                return redirect(url_for('go_hidric_cal_2'))
            elif page == 3:
                return redirect(url_for('go_hidric_cal_3'))
            elif page == 4:
                return redirect(url_for('go_hidric_cal_4'))
            elif page == 5:
                return redirect(url_for('go_hidric_cal_5'))

        return render_template('cal_hid.html', user = user_name, id = user_id, photo = photo)

@app.route('/hidric_cal_1', methods=['POST'])
def hidric_cal_1():
    if request.method == 'POST':
        if 'id' in session:
            id_user = session['id']

            #If this variable does not exist, then it's going to be assigned a traditional valor
            try:
                shower_type = request.form['shower_type']
            except:
                shower_type = 'not_value'
                
            minutes_shower = request.form['minutes_shower']
            shower_times = request.form['shower_times']
            
            total_shower = water_products_calculus.showers(minutes_shower, shower_type, shower_times)

            #If this variable does not exist, then it's going to be assigned a traditional valor
            try:
                toilet_type = request.form['toilet_type']
            except:
                toilet_type = 'not_value'
        
            bathroom_times = request.form['bathroom_times']
            print("bathroom times: ", bathroom_times)

            total_toilet = water_products_calculus.toilet(bathroom_times,toilet_type)



            cur = mysql.connection.cursor()
            cur.execute('CALL prd_calc_hidric_1 (%s, %s, %s)', (id_user, total_shower, total_toilet))
            mysql.connection.commit()

            if id_user != 10:
                cur.execute('UPDATE tuser_log SET hidric_page = 2 WHERE id_user = %s', (id_user,))
                mysql.connection.commit()

            return redirect(url_for('go_hidric_cal_2'))
        else:
            return 'you have to logged in first'

@app.route('/go_hidric_cal_2', methods=['GET'])
def go_hidric_cal_2():
    if request.method == 'GET':
        if 'id' in session:
            user_id = session['id']
            user_name = session['user']
            photo = session['img']
        return render_template('cal_hid_2.html', id = user_id, user = user_name, photo = photo)

@app.route('/hidric_cal_2', methods=['POST'])
def hidric_cal_2():
    if request.method == 'POST':
        if 'id' in session:
            user_id = session['id']
            #variables for cleaning 
            try:
                wash_type = request.form['wash_type']
            except:
                wash_type = 'not_value'
            #If this variable does not exist, then it's going to be assigned a traditional valor
        
            times_per_day_dishes = request.form['times_per_day_dishes']
            
            #If this variable does not exist, then it's going to be assigned a traditional valor
            try:
                by_hand_type = request.form['by_hand_type']
            except:
                by_hand_type = 0
                
            minutes_washing_dishes = request.form['minutes_washing_dishes']
            liters_by_hand = request.form['liters_by_hand']

            #variables for cleaning clothes
                        
            #If this variable does not exist, then it's going to be assigned a traditional valor
            try:
                washing_machine_type = request.form['washing_machine_type']
            except:
                washing_machine_type = 'not_value'
            #If this variable does not exist, then it's going to be assigned a traditional valor
                
            user_knows = 1
            washing_clothes_times = request.form['washing_clothes_times']

            #If this variable does not exist, then it's going to be assigned a traditional valor
            if washing_machine_type == 'dont_know':
                user_knows = 0

            total_dishes = water_products_calculus.dishes(wash_type, times_per_day_dishes, minutes_washing_dishes, by_hand_type, liters_by_hand)

            total_washing_machine = water_products_calculus.washing_clothest(washing_clothes_times, washing_machine_type, user_knows)

            cur = mysql.connection.cursor()
            cur.execute('CALL prd_calc_hidric_2 (%s, %s, %s);', (user_id, total_dishes, total_washing_machine))
            mysql.connection.commit()

            if user_id != 10:
                cur.execute('UPDATE tuser_log SET hidric_page = 3 WHERE id_user = %s', (user_id,))
                mysql.connection.commit()

            return redirect(url_for('go_hidric_cal_3'))
        else:
            return 'You have to log in first'

@app.route('/go_hidric_cal_3', methods=['GET'])
def go_hidric_cal_3():
    if 'id' in session:
        user_id = session['id']
        user_name = session['user']
        photo = session['img']
        return render_template('cal_hid_3.html', id = user_id, user = user_name, photo = photo)
    else:
        return 'You have to log in first'

@app.route('/hidric_cal_3', methods=['POST'])
def hidric_cal_3():
    if request.method == 'POST':
        if 'id' in session:
            user_id = session['id']
            #If this variable does not exist, then it's going to be assigned a traditional valor
            try:
                watering_type = request.form['watering_type']
            except:
                watering_type = 'not_value'
                
            watering_minutes = request.form['watering_minutes']
            yard_size = request.form['yard_size']
            liters_bottle = request.form['liters_bottle']
            times_watering = request.form['times_watering']
            drippers_number = request.form['drippers_number']
            try:
                flow_rate = request.form['flow_rate']
            except:
                flow_rate = 0

            total_watering_yard = water_products_calculus.garden_watering(watering_minutes, watering_type, liters_bottle, times_watering, yard_size, drippers_number, flow_rate)

            cur = mysql.connection.cursor()
            cur.execute('CALL prd_calc_hidric_3 (%s, %s);', (user_id, total_watering_yard))
            mysql.connection.commit()

            if user_id != 10:
                cur.execute('UPDATE tuser_log SET hidric_page = 4 WHERE id_user = %s', (user_id,))
                mysql.connection.commit()

            return redirect(url_for('go_hidric_cal_4'))
        else:
            return 'You have to log in first'

@app.route('/go_hidric_cal_4', methods=['GET'])
def go_hidric_cal_4():
    if 'id' in session:
        user_id = session['id']
        user_name = session['user']
        photo = session['img']
        return render_template('cal_hid_4.html', id = user_id, user = user_name, photo = photo)
    else:
        return 'You have to log in first'

@app.route('/hidric_cal_4', methods=['POST'])
def hidric_cal_4():
    if request.method == 'POST':
        if 'id' in session:
            user_id = session['id']

            mop_times = request.form['mop_times']
            buckets_number = request.form['buckets_number']
            liters_bucket = request.form['liters_bucket']

            total_cleaning_house = water_products_calculus.house_cleaning(liters_bucket, buckets_number, mop_times)

            cur = mysql.connection.cursor()

            cur.execute('CALL prd_calc_hidric_4 (%s, %s);', (user_id, total_cleaning_house))
            mysql.connection.commit()

            if user_id != 10:
                cur.execute('UPDATE tuser_log SET hidric_page = 5 WHERE id_user = %s', (user_id,))
                mysql.connection.commit()

            return redirect(url_for('go_hidric_cal_5'))
        else:
            return 'You have to log in first'

@app.route('/go_hidric_cal_5', methods=['GET'])
def go_hidric_cal_5():
    if 'id' in session:
        user_id = session['id']
        user_name = session['user']
        photo = session['img']
        return render_template('cal_hid_5.html', id = user_id, user = user_name, photo = photo)
    else:
        return 'You have to log in first'

@app.route('/hidric_cal_5', methods=['POST'])
def hidric_cal_5():
    if request.method == 'POST':
        if 'id' in session:
            user_id = session['id']

            cups_coffe = request.form['cups_coffe']
            total_coffe = water_products_calculus.coffe(cups_coffe)

            cups_tea = request.form['cups_tea']
            total_tea = water_products_calculus.tea(cups_tea)

            kg_beef = request.form['kg_beef']
            total_beef = water_products_calculus.cow_meat(kg_beef)

            kg_chicken = request.form['kg_chicken']
            total_chicken = water_products_calculus.chicken_meat(kg_chicken)

            pork_meat = request.form['pork_meat']
            total_pork = water_products_calculus.pork_meat(pork_meat)

            kg_rice = request.form['kg_rice']
            total_rice = water_products_calculus.rice(kg_rice)

            kg_sugar = request.form['kg_sugar']
            total_sugar = water_products_calculus.sugar(kg_sugar)

            kg_cheese = request.form['kg_cheese']
            total_cheese = water_products_calculus.cheese(kg_cheese)

            lt_milk = request.form['lt_milk']
            total_milk = water_products_calculus.milk(lt_milk)

            lt_beer = request.form['lt_beer']
            total_beer = water_products_calculus.beer(lt_beer)

            lt_juice = request.form['lt_juice']
            total_juice = water_products_calculus.processed_juice(lt_juice)

            lt_soda = request.form['lt_soda']
            total_soda = water_products_calculus.soda(lt_soda)

            eggs = request.form['eggs']
            total_eggs = water_products_calculus.eggs(eggs)

            bread_slices = request.form['bread_slices']
            total_bread = water_products_calculus.bread_slices(bread_slices)

            cur = mysql.connection.cursor()

            cur.execute('CALL prd_calc_hidric_5 (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', (user_id, total_coffe, total_tea, total_beef, total_chicken, total_pork, total_rice, total_sugar, total_cheese, total_milk, total_beer, total_juice, total_soda, total_eggs, total_bread))
            mysql.connection.commit()

            if user_id != 10:
                cur.execute('UPDATE tuser_log SET hidric_page = 1 WHERE id_user = %s', (user_id,))
                mysql.connection.commit()

            return redirect(url_for('final_hid_calculator'))
        else:
            return 'You have to log in'

@app.route('/final_hid_calculator', methods=['GET'])
def final_hid_calculator():
    if 'id' in session:
        user_id = session['id']
        user_name = session['user']
        photo = session['img']
        cur = mysql.connection.cursor()
        cur.execute('CALL prd_get_hidric_footprint (%s, @final_emission);', (user_id,))
        cur.execute('SELECT @final_emission;')
        total_water_footprint = cur.fetchall()

        formatted_value = "{:.2f}".format(total_water_footprint[0][0])


        return render_template('final_cal_hid.html', id = user_id, user = user_name, total = formatted_value, photo = photo)
    else:
        return 'You have to log in first'

@app.route('/go_cal_transport', methods=['GET'])
def go_cal_transport():
    if 'id' in session:
        user_id = session['id']
        user_name = session['user']
        photo = session['img']
        return render_template('cal_veh_1.html', id = user_id, user = user_name, photo = photo)
    else:
        return 'You have to log in first'
    
@app.route('/cal_transport', methods=['POST'])   
def cal_transport(): 
    if request.method == "POST":
        if 'id' in session:
            user_id = session['id']
            #Brings all the values from the form to send it at the method that do the calculus        
            fuel_type = request.form["fuel_type"]
            cylinder_count = int(request.form["cylinders_count"])
            vehicle_year = int(request.form["vehicule_old"])
            time_used = int(request.form["time_used"])
            consumed_fuel = int(request.form["consumed_fuel"])
            distance = int(request.form["distance_traveled"])
            #Brings from the db the emission factors and their ids
            cur = mysql.connection.cursor()
            cur.execute('CALL prd_get_vehicule_adjustments(%s, %s, %s, @year_adjustment, @cylinder_adjustment, @fuel_adjustment, @id_year_adjustment, @id_cyilinder_adjustment, @id_fuel_adjustment);', (vehicle_year, cylinder_count, fuel_type))
            cur.execute('SELECT @year_adjustment, @cylinder_adjustment, @fuel_adjustment, @id_year_adjustment, @id_cyilinder_adjustment, @id_fuel_adjustment')
            outputs_list = cur.fetchone()
            outputs_and_adjustments = list(outputs_list)            
            #Recieves two values from the merhod, the total factor and the fuel performance
            transport_emission , fuel_performance = transportCalculus.transportEmission(distance, consumed_fuel, outputs_and_adjustments[0], outputs_and_adjustments[1], outputs_and_adjustments[2])
            final_transport_emission = round(transport_emission, 2)
            print(f'Final emission: {final_transport_emission}')
            #Insert all the values returned to the db
            cur.execute('CALL prd_insert_calc_transport_emission(%s, %s, %s, %s, %s, %s, %s, %s, %s);', (user_id, outputs_and_adjustments[5], outputs_and_adjustments[4], outputs_and_adjustments[3], time_used, consumed_fuel, distance, fuel_performance, final_transport_emission))                        
            return redirect(url_for('go_cal_electric'))
#Redirects to the page that shows your emision
#Redirects to the page to do the electrical calculus
@app.route('/go_cal_electric', methods=['GET'])
def go_cal_electric():
    if 'id' in session:
        user_id = session['id']
        user_name = session['user']
        photo = session['img']
        return render_template('cal_electric.html', id = user_id, user = user_name, photo = photo)
    else:
        return 'You have to log in first'
    
@app.route('/cal_electric', methods=['POST'])
def cal_electric():
    if request.method == 'POST':
        if 'id' in session:
            devices_used = list()#In this dict, is going to save all the infor os the usage of each device
            cur = DbConection.get_dict_cursor()

            devices_selectes_list = request.form.getlist('device')#Brings all the chekboxes selected
            print("Dispositivos seleccionados: ", len(devices_selectes_list))

            for device in devices_selectes_list:
                device_info = {'id_device': 0, 'name': '', 'device_active_power': 0.0, 'active_used_hours': 0.0, 'device_standby_power': 0.0, 'standby_used_hours': 0.0, 'device_efficiency': 0.0}                
                cur.execute("SELECT device_name FROM tcat_device WHERE id_device = %s;", (device,))
                device_info['name'] = cur.fetchone()['device_name']
                device_info['id_device'] = device
                devices_used.append(device_info)

            print('Lista de diccionarios": ',devices_used)
            print('Nombre del primer dispositivo: ', devices_used[0]['name'])
            session['devices_selected'] = devices_used#Saves the list to be able to access to it in any part
            return redirect(url_for('go_electric_devices_info'))
        else:
            return 'You have to log in first'
        
@app.route('/go_electric_devices_info', methods=['GET'])
def go_electric_devices_info():
    if 'id' in session:
        user_id = session['id']
        user_name = session['user']
        photo = session['img']
        devices_selected_list = session.get('devices_selected', [])
        print('DISPOSITIVOS ANTES DE SER ENVIADOS AL FORM DE INFO: ', devices_selected_list)
        return render_template('cal_electric_device_info.html', id = user_id, user = user_name, devices_list = devices_selected_list, photo = photo)

@app.route('/electric_devices_info', methods=['POST'])
def electric_devices_info():
    if request.method == "POST":
        if 'id' in session:
            user_id = session['id']
            cur = mysql.connection.cursor()
            device_ids = request.form.getlist('device_id')
            active_powers = request.form.getlist('device_active_power')
            active_hours = request.form.getlist('active_used_hours')
            standby_powers = request.form.getlist('device_standby_power')
            standby_hours = request.form.getlist('standby_used_hours')
            device_efficiencies = request.form.getlist('device_efficiency')
            #Dictionary that saves the dictionaries generated for each device
            devices_data = []
            print('IDS DE LOS DISPOSITIVOS REGRESADOS POR EL FORM CON INFO: ', device_ids)
            #Iterate each device data recolected from the form
            for i in range(len(device_ids)):
                device_data = {
                    'device_id': int(device_ids[i]),
                    'active_power': float(active_powers[i]),
                    'active_hour': float(active_hours[i]),
                    'standby_power': float(standby_powers[i]),
                    'standby_hour': float(standby_hours[i]),
                    'device_efficiency': float(device_efficiencies[i]),
                }
                #Saves each dictionary generated for each device
                devices_data.append(device_data)
                print('Lista final', devices_data[i])

            for device in devices_data:
                if device['device_efficiency'] == 0:
                    device['device_efficiency'] = 1
                else:
                    device['device_efficiency'] = device['device_efficiency'] / 100
                cur.execute("CALL prd_insert_devices_values(%s, %s, %s, %s, %s, %s, %s);", (user_id, device['device_id'], device['active_power'], device['active_hour'], device['standby_power'], device['standby_hour'], device['device_efficiency']))
                print('Lista final', device)

            cur.execute("CALL prd_calculate_total_energy_emission(%s);", (user_id,))
            return redirect(url_for('go_cal_carbon_products'))
        else:
            return 'You have to log in first'
      
@app.route('/go_cal_water_products', methods=['GET'])
def go_cal_water_products():
    if 'id' in session:
        user_id = session['id']
        user_name = session['user']
        photo = session['img']
        return render_template('cal_water_products.html', id = user_id, user = user_name, total = 1, photo = photo)
    else:
        return 'You have to log in first'  
    
@app.route('/cal_water_products', methods=['POST'])
def cal_water_products():
    if request.method == 'POST':
        if 'id' in session:
            user_id = session['id']
            cold_water = 0
            hot_water = 0
            #Brings the information of the user from the frontend
            water_consumed = int(request.form['water_consumed'])
            water_heated_percentage = int(request.form['water_heated_percentage'])
            id_heater_type = int(request.form['heater_type'])
            #Compares the heater
            if id_heater_type == 5:
                water_heated_percentage = 0
            #Percentages of each type of water temperature
            cold_water_percentage = 100 - water_heated_percentage
            hot_water_percentage = 100 - cold_water_percentage
            #Print all values obtained
            print('Percentage of cold water: ', cold_water_percentage)
            print('Percentage of hot water: ', hot_water_percentage)
            print('Id of the type of heater: ', id_heater_type)
            #Round the values to an easy handle of them
            hot_water = round((water_consumed * hot_water_percentage) / 100)
            cold_water = round((water_consumed * cold_water_percentage) / 100)
            print('Cold water: ', cold_water)
            print('Hot water', hot_water)
            #Prd that inserts all the values obtained            
            cur = mysql.connection.cursor()
            cur.execute("CALL prd_new_calc_water_emission(%s, %s, %s, %s);", (user_id, cold_water, hot_water, id_heater_type))
            return redirect(url_for('go_final_cal_carbon_footprint'))
        else:
            return 'You have to log in first'
    
@app.route('/go_cal_carbon_products', methods=['GET'])
def go_cal_carbon_products():
    if 'id' in session:
        if session['id'] != 10:
            user_id = session['id']
            user_name = session['user']
            photo = session['img']
            return render_template('cal_carbon_products.html', id = user_id, user = user_name, photo = photo)
        return 'you have to log in first'
    return 'you have to log in first'

@app.route('/cal_carbon_products', methods=['POST'])
def cal_carbon_products():
    if request.method == 'POST':
        if 'id' in session:
            
            user_id = session['id']
            
            #First of all, it's necessary call the answers of the user on the frontend which are the how many products the user consume (the name of the unit depends of the kind product, for example for the meat, we use kg)   
            cow_meat_kg = int(request.form['cow_meat_kg'])
            pork_meat_kg = int(request.form['pork_meat_kg'])
            chicken_meat_kg = int(request.form['chicken_meat_kg'])
            
            #Now, we bring the data about the transport, packaging and refrigeration of the products and we are bringing these data in each topic (meat, dairy, fruits)
            meat_transport = request.form['meat_transport']
            meat_packaging = request.form['meat_packaging']
            meat_refrigeration = request.form['meat_refrigeration']
            
            #I made a function that its process send the information to the database, the first parameter is the id of the product (you can see it on the database, in this case is 1), the second parameter is the unit (in this case is the cow meat kg), the next parameter is the transport, the next parameter is the packaging, the next parameter is the refrigeration and finally, the last parameter is the user id which was declarated before
            send_emission = products_adjustements(1, cow_meat_kg, meat_transport, meat_packaging, meat_refrigeration, user_id)
            #If the function returns a 0 it means that there is an error, and I made this to find easier the error
            if send_emission == 0:
                return 'There is an error sending cow meat product carbon emission'
            #the process of sending the information it will be necessary in each product
            send_emission = products_adjustements(2, pork_meat_kg, meat_transport, meat_packaging, meat_refrigeration, user_id)
            if send_emission == 0:
                return 'There is an error sending pork meat product carbon emission'
            
            send_emission = products_adjustements(3, chicken_meat_kg, meat_transport, meat_packaging, meat_refrigeration, user_id)
            if send_emission == 0:
                return 'There is an error sending chicken product carbon emission'
            #Dairy
            #And now, the process is repeated in each topic (in this case is dairy)
            milk_liters = int(request.form['milk_liters'])
            cheese_kg = int(request.form['cheese_kg'])
            dairy_transport = request.form['dairy_transport']
            dairy_packaging = request.form['dairy_packaging']
            dairy_refrigeration = request.form['dairy_refrigeration']
            
            send_emission = products_adjustements(4, milk_liters, dairy_transport, dairy_packaging, dairy_refrigeration, user_id)
            if send_emission == 0:
                return 'There is an error sending milk product carbon emission'
            
            send_emission = products_adjustements(5, cheese_kg, dairy_transport, dairy_packaging, dairy_refrigeration, user_id)
            if send_emission == 0:
                return 'There is an error sending cheese product carbon emission'
            
            #Fruits
            local_production_kg = int(request.form['local_production_kg'])
            greenhouse_production_kg = int(request.form['greenhouse_production_kg'])
            imported_production_kg = int(request.form['imported_production_kg'])
            
            fruits_transport = request.form['fruits_transport']
            fruits_packaging = request.form['fruits_packaging']
            fruits_refrigeration = request.form['fruits_refrigeration']
            
            send_emission = products_adjustements(6, local_production_kg, fruits_transport, fruits_packaging, fruits_refrigeration, user_id)
            if send_emission == 0:
                return 'There is an error sending local production product carbon emission'
            
            send_emission = products_adjustements(7, greenhouse_production_kg, fruits_transport, fruits_packaging, fruits_refrigeration, user_id)
            if send_emission == 0:
                return 'There is an error sending greenhouse production product carbon emission'
            
            send_emission = products_adjustements(8, imported_production_kg, fruits_transport, fruits_packaging, fruits_refrigeration, user_id)
            if send_emission == 0:
                return 'There is an error sending imported production product carbon emission'
            
            #Clothes
            t_shirt_unit = int(request.form['t_shirt_unit'])
            denim_pants_unit = int(request.form['denim_pants_unit'])
            shoes_unit = int(request.form['shoes_unit'])
            
            clothes_transport = request.form['clothes_transport']
            clothes_packaging = request.form['clothes_packaging']
            
            send_emission = products_adjustements(9, t_shirt_unit, clothes_transport, clothes_packaging, 8, user_id)
            if send_emission == 0:
                return 'There is an error sending tshirt product carbon emission'
            
            send_emission = products_adjustements(10, denim_pants_unit, clothes_transport, clothes_packaging, 8, user_id)
            if send_emission == 0:
                return 'There is an error sending denim pants product carbon emission'
            
            send_emission = products_adjustements(11, shoes_unit, clothes_transport, clothes_packaging, 8, user_id)
            if send_emission == 0:
                return 'There is an error sending shoes product carbon emission'
            
            #Electronic devices
            cellphone_unit = int(request.form['cellphone_unit'])
            laptop_unit = int(request.form['laptop_unit'])
            television_unit = int(request.form['television_unit'])
            
            electronic_transport = request.form['electronic_transport']
            electronic_packaging = request.form['electronic_packaging']
            
            send_emission = products_adjustements(12, cellphone_unit, electronic_transport, electronic_packaging, 8, user_id)
            if send_emission == 0:
                return 'There is an error sending cellphone product carbon emission'
            
            send_emission = products_adjustements(13, laptop_unit, electronic_transport, electronic_packaging, 8, user_id)
            if send_emission == 0:
                return 'There is an error sending laptop product carbon emission'
            
            send_emission = products_adjustements(14, television_unit, electronic_transport, electronic_packaging, 8, user_id)
            if send_emission == 0:
                return 'There is an error sending television product carbon emission'
            
            #Cleaning products
            detergent_kg = int(request.form['detergent_kg'])
            softener_lt = int(request.form['softener_lt'])
            all_purpose_lt = int(request.form['all_purpose_lt'])
            
            cleaning_transport = request.form['cleaning_transport']
            cleaning_packaging = request.form['cleaning_packaging']
            
            send_emission = products_adjustements(15, detergent_kg, cleaning_transport, cleaning_packaging, 8, user_id)
            if send_emission == 0:
                return 'There is an error sending detergent product carbon emission'
            
            send_emission = products_adjustements(16, softener_lt, cleaning_transport, cleaning_packaging, 8, user_id)
            if send_emission == 0:
                return 'There is an error sending softener product carbon emission'
            
            send_emission = products_adjustements(17, all_purpose_lt, cleaning_transport, cleaning_packaging, 8, user_id)
            if send_emission == 0:
                return 'There is an error sending all purpose product carbon emission'
            
            return redirect(url_for('go_cal_water_products'))

    return 'You have to log in first'
#This is the function that receives the parameters and will send the information and the final emission of each product to the database.
def products_adjustements(product_id, product_unit, transport, packaging, refrigeration, user_id):
    cur = mysql.connection.cursor()
    product_unit = float(product_unit)
    #The funcion in this part takes the different adjustements
    cur.execute('CALL prd_new_carbon_product_adjustements(%s, %s, %s, %s, %s, @carbon_emission, @transport_adjustement, @packaging_adjustement, @refrigeration_adjustement);', (user_id, product_id, transport, packaging, refrigeration))
    cur.execute('SELECT @carbon_emission, @transport_adjustement, @packaging_adjustement, @refrigeration_adjustement;')
    adjustements = cur.fetchone()
        
    #It adds the different adjustements in variables
    carbon_emission = float(adjustements[0])
    transport_adjustement = float(adjustements[1])
    packaging_adjustement = float(adjustements[2])
    refrigeration_adjustement = float(adjustements[3])
        
    #it sends the adjustements and the units of the product to calculate the final emission and return it into a variable
    final_emission = float(carbon_products_calculus.product_carbon_emission(product_unit, carbon_emission, transport_adjustement, packaging_adjustement, refrigeration_adjustement))
    print(final_emission)
        
    #Here it inserts the result on the database
    cur.execute('CALL prd_insert_product_carbon_emission(%s, %s, %s, %s)', (user_id, product_id, product_unit, final_emission,))
    mysql.connection.commit()
        
    successful = 1

    return successful

@app.route('/go_final_cal_carbon_footprint', methods=['GET'])
def go_final_cal_carbon_footprint():
    if request.method == 'GET':
        if 'id' in session:
            user_id = session['id']
            user_name = session['user']
            photo = session['img']
            #HERE IS WHERE GRAFANA SHOULD BE. THIS MESSAGE IS FOR JOSUE
            return render_template('final_carbon_emission.html', id = user_id, user = user_name, photo = photo)
    return 'You must log in before'

@app.route('/update_data', methods=['POST'])
def update_data():
    if request.method == 'POST':
        if 'id' in session:
            user_id = session['id']
            
            cur = mysql.connection.cursor()
            
            new_user_name = request.form['username']
            if not new_user_name:
                new_user_name = session['user']
            
            new_first_name = request.form['first_name']
            if not new_user_name:
                new_first_name = session['first_name']
            
            new_last_name = request.form['last_name']
            if not new_last_name:
                new_last_name = session['last_name']
                
            new_email = request.form['email']
            if not new_email:
                new_email = session['email']
                
            file     = request.files['select_img']
            
            if file:
                cur.execute('SELECT user_img_path FROM tusers WHERE id_user = %s', (user_id,))
                photo = cur.fetchone()[0]
                if photo:
                    basepath = os.path.dirname (__file__) #C:\xampp\htdocs\elmininar-archivos-con-Python-y-Flask\app
                    url_File = os.path.join (basepath, 'static/user_img', photo)
                    if os.path.exists(url_File):
                        os.remove(url_File)
            
            basepath = os.path.dirname (__file__) #La ruta donde se encuentra el archivo actual
            filename = secure_filename(file.filename) #Nombre original del archivo
                    
            #capturando extensión del archivo ejemplo: (.png, .jpg, .pdf ...etc)
            extension           = os.path.splitext(filename)[1]
            
            if extension == '.jpg' or extension == '.jpeg' or extension == '.png' or extension == '.webp':
            
                newNameFile     = random_string() + extension
                
                upload_path = os.path.join (basepath, 'static/user_img', newNameFile) 
                file.save(upload_path)
                
                session.pop('img', None)
                session['img'] = newNameFile
                
                cur.execute('UPDATE tusers SET user_img_path = %s WHERE id_user = %s', (newNameFile, user_id))
                mysql.connection.commit()
            else:
                flash('You must put a image file')
                
            session.pop('user', None)
            session.pop('first_name', None)
            session.pop('last_name', None)
            session.pop('email', None)
                
            session['user']= new_user_name
            session['first_name']= new_first_name
            session['last_name']= new_last_name
            session['email']= new_email
                
            cur.execute('UPDATE tusers SET first_name = %s, last_name = %s, user_name = %s, user_mail = %s WHERE id_user = %s', (new_first_name, new_last_name, new_user_name, new_email, user_id))
            mysql.connection.commit()
            return redirect(url_for('go_user_profile'))

#This is a method that recieves an error and renderising the error handle page
@app.route('/page_not_found')
def page_not_found(error):
    if 'id' in session:
        user_id = session['id']
        user_name = session['user']
        return render_template("404.html", id = user_id, user = user_name), 404

def user_render_page(pageToRender):
    if 'id' in session:
        user_id = session['id']
        user_name = session['user']
        return render_template(f'{pageToRender}', id = user_id, user = user_name)
    else:
        return 'You have to log in first'
    
def random_string():
    random_string = "0123456789abcdefghijklmnopqrstuvwxyz_"
    length         = 20
    secuencia        = random_string.upper()
    random_result  = sample(secuencia, length)
    random_string     = "".join(random_result)
    return random_string


    
#This is for running the application as a server
if __name__ == "__main__":
    #This prevents that appears an error of page not found and shows a error handle page
    #app.register_error_handler(404, page_not_found)
    app.run(port= 5000, debug=True)