from flask import Blueprint, request, jsonify, session
from app.models.authentication_model import AuthenticationModel
from functools import wraps
from typing import Dict, Any, Callable
import re

bp = Blueprint("auth_routes", __name__)

def login_required(f: Callable) -> Callable:
    """Decorator to protect routes that require authentication"""
    @wraps(f)
    def decorated_function(*args: Any, **kwargs: Any) -> Any:
        if 'username' not in session:
            return jsonify({'status': 'error', 'message': 'Authentication required'}), 401
        return f(*args, **kwargs)
    return decorated_function

def validate_request_data(data: Dict[str, Any], required_fields: list) -> tuple[bool, str]:
    """Validate request data contains all required fields"""
    if not data:
        return False, "No data provided"
    
    missing_fields = [field for field in required_fields if field not in data or not data[field]]
    if missing_fields:
        return False, f"Missing required fields: {', '.join(missing_fields)}"
    
    return True, ""

@bp.route('/sign_up_service', methods=["POST"])
def sign_up_service():
    """
    Handle user registration.
    
    Expected JSON payload:
    {
        "firstname": str,
        "lastname": str,
        "username": str,
        "password": str,
        "confirm-password": str,
        "email": str
    }
    
    Returns:
        JSON response with status and message
    """
    try:
        user_info = request.get_json()
        required_fields = ['firstname', 'lastname', 'username', 'password', 'confirm-password', 'email']
        
        # Validate request data
        is_valid, error_message = validate_request_data(user_info, required_fields)
        if not is_valid:
            return jsonify({'status': 'error', 'message': error_message}), 400
            
        # Validate password confirmation
        if user_info['password'] != user_info['confirm-password']:
            return jsonify({'status': 'error', 'message': 'Password confirmation does not match'}), 400
            
        # Create user
        authen_model = AuthenticationModel()
        result = authen_model.create_user(user_info)
        
        if result['status'] == 'success':
            return jsonify(result), 201
        else:
            return jsonify(result), 400
        
    except Exception as error:
        return jsonify({'status': 'error', 'message': str(error)}), 500

@bp.route('/login_service', methods=["POST"])
def login_service():
    """
    Handle user login.
    
    Expected JSON payload:
    {
        "username": str,
        "password": str
    }
    
    Returns:
        JSON response with status and user data if successful
    """
    try:
        data = request.get_json()
        required_fields = ['username', 'password']
        
        # Validate request data
        is_valid, error_message = validate_request_data(data, required_fields)
        if not is_valid:
            return jsonify({'status': 'error', 'message': error_message}), 400

        # Authenticate user
        authen_model = AuthenticationModel()
        user = authen_model.get_user(data)
        
        if not user:
            return jsonify({'status': 'error', 'message': 'Invalid credentials'}), 401
        
        # Set session data
        session['id'] = str(user['_id'])
        session['username'] = user['user_name']
        session['email'] = user['email']
 
        return jsonify({
            'status': 'success',
            'message': 'Login successful',
            'user': {
                'username': user['user_name'],
                'email': user['email']
            }
        }), 200
        
    except Exception as error:
        return jsonify({'status': 'error', 'message': str(error)}), 500

@bp.route('/logout', methods=['GET'])
@login_required
def logout():
    """
    Handle user logout by clearing the session.
    
    Returns:
        JSON response with status and message
    """
    try:
        session.clear()
        return jsonify({
            'status': 'success',
            'message': 'Logout successful'
        }), 200
    except Exception as error:
        return jsonify({
            'status': 'error',
            'message': str(error)
        }), 500