from flask import Blueprint, request, jsonify, session
from app.models.authentication_model import AuthenticationModel

bp = Blueprint("authentication", __name__)

authenModel = AuthenticationModel()

@bp.route('/sign_up_service', methods=["POST"])
def sign_up_service():
    try:
        # gets the data provided by the fetch
        response = request.get_json() 
        # is saved in by separated
        username = response.get("username")
        email = response.get("email")
        password = response.get("password")
        
        if not username or not email or not password:
            status = "Invalid input."
            return jsonify({"Status": status}), 400
        
        elif(response['password'] == response['confirm-password']):
            # call model to insert data
            status = authenModel.insert_user(username, email, password)  
            return jsonify({"Status": status})
        
        else:
            status = "Password confirmation incorrect, verify your credentials."
            return jsonify({"Status": status})
    except KeyError as error:
            return jsonify({"Status": status}, error)

@bp.route('/login_service', methods=["POST"])
def login_service():
    try:
        # gets the data provided by the fetch
        response = request.get_json() 
        username = str(response.get("username"))
        password = str(response.get("password"))
        
        # call model to get the user if exist
        response = authenModel.get_user(username, password) #example: (3, 'CleanUser', 'cleanlyfe_user@gmail.com')
        
        # if there is no response
        if response == None:
            # change the type of status and return
            status = "Login error, incorrect credentials."
            return jsonify({"Status": status}), 401
        else:
            # change the type of status
            status = 'Login successfull.'
            # saves the session
            session["id"] = response[0]
            session["username"] = response[1]
            session["email"] = response[2]
            
            return jsonify({"Status": status}), 201
    except KeyError as error:
        return jsonify({"Status": "Something went wrong when logging in, try later."}, error), 401
    
@bp.route('/logout', methods=['GET'])
def logout():
    if 'username' in session:
        session.clear() # clears the session
        status = "Log out successfull."
    return jsonify({"Status": status})