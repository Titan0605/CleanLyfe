from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_mysqldb import MySQL
import water_products_calculus
import transportCalculus, DbConection
import pymysql

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
        return render_template('index.html')
    return render_template('index.html')

@app.route('/register_fun', methods=['POST'])
def register_fun():
    if request.method == 'POST':
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
                cur.execute('INSERT INTO tusers (id_type_member, user_name, user_email, user_password, active, created_at) VALUES (1, %s, %s, %s, 1, NOW())', (user_name, email, password))
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
        return render_template('userProfile.html')

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
        if user == 'invited':
            return render_template('404.html')
        else:
            return render_template('cleanlyfe.html', user = user)


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
                return render_template('misions.html', user = user_name)
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
            
        else:
            session['id']= int(10)
            session['user']='invited'
            user_id = session['id']
            user_name = session['user']

        if user_id != 10:
            cur = mysql.connection.cursor()
            cur.execute('SELECT page_water_footprint FROM tuser_log WHERE id_user = %s', (user_id,))
            data = cur.fetchone()
            page = data[0]
            if page == 1:
                return render_template('cal_hid.html', user = user_name, id = user_id)
            elif page == 2:
                return redirect(url_for('go_hidric_cal_2'))
            elif page == 3:
                return redirect(url_for('go_hidric_cal_3'))
            elif page == 4:
                return redirect(url_for('go_hidric_cal_4'))
            elif page == 5:
                return redirect(url_for('go_hidric_cal_5'))

        return render_template('cal_hid.html', user = user_name, id = user_id)

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
            cur.execute('CALL prd_calc_hidric_beginnn (%s, %s, %s)', (id_user, total_shower, total_toilet))
            mysql.connection.commit()

            if id_user != 10:
                cur.execute('UPDATE tuser_log SET page_water_footprint = 2 WHERE id_user = %s', (id_user,))
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
        return render_template('cal_hid_2.html', id = user_id, user = user_name)

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
            cur.execute('CALL cal_hidric_two (%s, %s, %s);', (user_id, total_dishes, total_washing_machine))
            mysql.connection.commit()

            if user_id != 10:
                cur.execute('UPDATE tuser_log SET page_water_footprint = 3 WHERE id_user = %s', (user_id,))
                mysql.connection.commit()

            return redirect(url_for('go_hidric_cal_3'))
        else:
            return 'You have to log in first'

@app.route('/go_hidric_cal_3', methods=['GET'])
def go_hidric_cal_3():
    if 'id' in session:
        user_id = session['id']
        user_name = session['user']
        return render_template('cal_hid_3.html', id = user_id, user = user_name)
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
            cur.execute('CALL cal_hidric_three (%s, %s);', (user_id, total_watering_yard))
            mysql.connection.commit()

            if user_id != 10:
                cur.execute('UPDATE tuser_log SET page_water_footprint = 4 WHERE id_user = %s', (user_id,))
                mysql.connection.commit()

            return redirect(url_for('go_hidric_cal_4'))
        else:
            return 'You have to log in first'

@app.route('/go_hidric_cal_4', methods=['GET'])
def go_hidric_cal_4():
    if 'id' in session:
        user_id = session['id']
        user_name = session['user']
        return render_template('cal_hid_4.html', id = user_id, user = user_name)
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

            cur.execute('CALL cal_hidric_four (%s, %s);', (user_id, total_cleaning_house))
            mysql.connection.commit()

            if user_id != 10:
                cur.execute('UPDATE tuser_log SET page_water_footprint = 5 WHERE id_user = %s', (user_id,))
                mysql.connection.commit()

            return redirect(url_for('go_hidric_cal_5'))
        else:
            return 'You have to log in first'

@app.route('/go_hidric_cal_5', methods=['GET'])
def go_hidric_cal_5():
    if 'id' in session:
        user_id = session['id']
        user_name = session['user']
        return render_template('cal_hid_5.html', id = user_id, user = user_name)
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

            cur.execute('CALL prd_cal_hidric_final (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', (user_id, total_coffe, total_tea, total_beef, total_chicken, total_pork, total_rice, total_sugar, total_cheese, total_milk, total_beer, total_juice, total_soda, total_eggs, total_bread))
            mysql.connection.commit()

            if user_id != 10:
                cur.execute('UPDATE tuser_log SET page_water_footprint = 1 WHERE id_user = %s', (user_id,))
                mysql.connection.commit()

            return redirect(url_for('final_hid_calculator'))
        else:
            return 'You have to log in'

@app.route('/final_hid_calculator', methods=['GET'])
def final_hid_calculator():
    if 'id' in session:
        user_id = session['id']
        user_name = session['user']
        cur = mysql.connection.cursor()
        cur.execute('SELECT water_footprint.total_water FROM water_footprint WHERE id_water_footprint = (SELECT MAX(id_water_footprint) FROM footprints_user WHERE id_user = %s);', (user_id,))
        total_water_footprint = cur.fetchall()

        formatted_value = "{:.2f}".format(total_water_footprint[0][0])


        return render_template('final_cal_hid.html', id = user_id, user = user_name, total = formatted_value)
    else:
        return 'You have to log in first'

@app.route('/go_cal_transport', methods=['GET'])
def go_cal_transport():
    if 'id' in session:
        user_id = session['id']
        user_name = session['user']
        return render_template('cal_veh_1.html', id = user_id, user = user_name)
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
            return redirect(url_for('final_cal_transport'))
#Redirects to the page that shows your emision
@app.route('/final_cal_transport', methods=['GET'])    
def final_cal_transport():
    if 'id' in session:
        user_id = session['id']
        user_name = session['user']
        cur = mysql.connection.cursor()    
        cur.execute('SELECT ttransport_emission.transport_emission FROM tuser_footprint JOIN tfootprints_records ON tuser_footprint.id_footprint_record = tfootprints_records.id_footprint_record JOIN tcarbon_footprint ON tfootprints_records.id_carbon_footprint = tcarbon_footprint.id_carbon_footprint JOIN ttransport_emission ON tcarbon_footprint.Id_transport_emission = ttransport_emission.Id_transport_emission WHERE tfootprints_records.id_footprint_record = ( SELECT MAX(id_footprint_record) FROM tfootprints_records AS record WHERE tfootprints_records.id_footprint_record = tuser_footprint.id_footprint_record AND tuser_footprint.Id_user = %s);', (user_id,))
        emission = cur.fetchall()
        formatted_value = "{:.2f}".format(emission[0][0])
        return render_template('final_cal_transport.html', id = user_id, user = user_name, total = formatted_value)
    else:
        return 'You have to log in first'
#Redirects to the page to do the electrical calculus
@app.route('/go_cal_electric', methods=['GET'])
def go_cal_electric():
    if 'id' in session:
        user_id = session['id']
        user_name = session['user']
        return render_template('cal_electric.html', id = user_id, user = user_name)
    else:
        return 'You have to log in first'
@app.route('/cal_electric', methods=['POST']) 
def cal_electric():
    if request.method == 'POST':
        if 'id' in session:
            finalList = []#En este dict se van a guardar todos los dict traidos de la db
            cur = DbConection.get_dict_cursor()
            
            mylist = request.form.getlist('device')#Trae los checkbox seleccionados
            print("valores en la lista: ", mylist)
            # for name in mylist:
            #     name = name.strip("'").strip('"') 
            #     print("Nombres:", name)       
            #     cur.execute("SELECT * FROM people WHERE name = %s;", (name,))
            #     rows = cur.fetchall()        
            #     for row in rows:
            #         finalList.append(row)                            
            # print(f"Cada lista: {finalList}")
            # print(f"Sacando algo en especifico: {finalList[2].get('age')}")
            return redirect(url_for('final_cal_electric'))        
        else:
            return 'You have to log in first'
        
@app.route('/final_cal_electric', methods=['GET'])
def final_cal_electric():
    if 'id' in session:
        user_id = session['id']
        user_name = session['user']        
        
        return render_template('final_cal_electric.html', id = user_id, user = user_name, total = 1)
    else:
        return 'You have to log in first'
@app.route('/go_cal_water_products', methods=['GET'])
def go_cal_water_products():
    if 'id' in session:
        user_id = session['id']
        user_name = session['user']
        return render_template('cal_water_products.html', id = user_id, user = user_name, total = 1)
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
            cur.execute("CALL prd_calc_water_emission(%s, %s, %s, %s);", (user_id, cold_water, hot_water, id_heater_type))
            return redirect(url_for('final_cal_electric'))
        else:
            return 'You have to log in first'
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
    
#This is for running the application as a server
if __name__ == "__main__":
    #This prevents that appears an error of page not found and shows a error handle page
    app.register_error_handler(404, page_not_found)
    app.run(port= 5000, debug=True)