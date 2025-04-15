from flask import Blueprint, request, jsonify

bp = Blueprint("authentication", __name__)

@bp.route('/sign_up', methods=["POST"])
def sign_up():
    # gets the data provided by the fetch
    response = request.get_json() 
    # if the password is the same
    if(response['password'] == response['confirm-password']):
        # call model to insert data
        
        return jsonify({"Status": "User created successfully."}), 201
    else:
        return jsonify({"Status": "User creation error."})
    
@bp.route('/login', methods=["POST"])
def login():
    # gets the data provided by the fetch
    response = request.get_json() 
    # call model to be sure is in db
    
    # if the password is the same
    if(True):        
        return jsonify({"Status": "Login successfull."}), 201
    else:
        return jsonify({"Status": "Login error."})