from flask import Blueprint, request, jsonify, session

bp = Blueprint("authentication", __name__)

@bp.route('/sign_up_service', methods=["POST"])
def sign_up_service():
    # gets the data provided by the fetch
    response = request.get_json() 
    print(response)
    # if the password is the same
    if(response['password'] == response['confirm-password']):
        # call model to insert data
        print("Password correct")
        return jsonify({"Status": "Login successfull."}), 201
    else:
        print("Password incorrect")
        return jsonify({"Status": "User creation error."})


@bp.route('/login_service', methods=["POST"])
def login_service():
    # gets the data provided by the fetch
    response = request.get_json() 
    # call model to be sure is in db
    print("Login service: ", response)
    # if the password is the same
    # if(True):        
    return jsonify({"Status": "Login successfull."}), 201
    # else:
    #     return jsonify({"Status": "Login error."})