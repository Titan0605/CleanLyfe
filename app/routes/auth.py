from flask import Blueprint, request, jsonify, session
from app.models.authentication_model import AuthenticationModel

bp = Blueprint("authentication", __name__)

authenModel = AuthenticationModel()

@bp.route('/sign_up_service', methods=["POST"])
def sign_up_service():
    try:
        # gets the data provided by the fetch
        response = request.get_json() 
        print(response)
        username = response.get("username")
        email = response.get("email")
        password = response.get("password")
        
        # if the password is the same
        if(response['password'] == response['confirm-password']):
            # call model to insert data
            status = authenModel.insert_user(username, email, password)  
            print(status)  
            return jsonify({"Status": status}), 201
        else:
            print(status)  
            return jsonify({"Status": status})
    except KeyError as error:
            print(status)  
            return jsonify({"Status": status}, error)

@bp.route('/login_service', methods=["POST"])
def login_service():
    try:
        # gets the data provided by the fetch
        response = request.get_json() 
        username = response.get("username")
        password = response.get("password")
        
        # call model to get the user if exist
        user = authenModel.get_user(username, password)
        print("User model response: ", user)
        if user == None:
            return jsonify({"status": "Login error, credentials incorrects."}), 401
        else:
            session["user"] = user
    except KeyError as error:
        return jsonify({"Status": "Login successfull."}, error), 401