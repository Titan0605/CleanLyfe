from flask import Blueprint, request, jsonify, session
from app.models.authentication_model import AuthenticationModel

bp = Blueprint("auth_routes", __name__)

@bp.route('/sign_up_service', methods=["POST"])
def sign_up_service():
    try:
        authenModel = AuthenticationModel()
        # gets the data provided by the fetch
        data = request.get_json() 
        
        user_info = dict(data)
        
        if not user_info or not user_info["userName"] or not user_info["password"]:
            return jsonify({'error': 'Email and password are required'}), 400
        
        if(user_info['password'] != user_info['confirm-password']):
            status = "Password confirmation incorrect, verify your credentials."
            return jsonify({"Status": status}), 401
            # call model to insert data
            
        status = authenModel.create_user(user_info)  
        return jsonify({"Status": status})
    except Exception as error:
            return jsonify({"Status": status, "Error": str(error)}), 401

@bp.route('/login_service', methods=["POST"])
def login_service():
    try:
        authenModel = AuthenticationModel()
        # gets the data provided by the fetch
        response = request.get_json()
        
        user_credentials = dict(response)
        
        if not user_credentials or not user_credentials["userName"] or not user_credentials["password"]:
            return jsonify({'error': 'Email and password are required'}), 400

        # call model to get the user if exist
        user = authenModel.get_user(user_credentials)
        
        # if there is no response
        if user == None or user["password"] != user_credentials["password"]:
            # change the type of status and return
            status = "Login error, incorrect credentials."
            return jsonify({"Status": status}), 401
        
        # change the type of status 
        status = 'Login successfull.'
        # saves the session
        session["id"] = str(user['_id'])
        session["username"] = user['userName']
        session["email"] = user['email']
        
        return jsonify({"Status": status}), 201
    except KeyError as error:
        return jsonify({"Status": "Something went wrong when logging in, try later.", "Error": str(error)}), 401
    
@bp.route('/logout', methods=['GET'])
def logout():
    if 'username' in session:
        session.clear() # clears the session
        status = "Log out successfull."
    return jsonify({"Status": status})