from flask import Blueprint, Response, render_template, redirect, url_for, request, jsonify
from app.services.hydric.hydricfp_calculus import HidricCalculator, calculate_consumption
from app.models.hydric_products_model import Hydric_products_model

bp = Blueprint("hydricfp_routes", __name__)

@bp.route('/hydricfp/calculation', methods=['POST'])
def calculate_hidric_footprint() -> Response:
    calculator = HidricCalculator()
    hidric_model = Hydric_products_model()
    try:
        data = request.get_json()
        print(data)
        
        calculations = calculate_consumption(calculator, data)
        
        print(calculations)
        
        response = hidric_model.save_hydric_footprint(calculations)
    
        render_template("home.html")
        return jsonify({'status': 'Data saved in DB', 'msg': str(response['message'])})
    except Exception as error:
        return jsonify({'status': f'Invalid value: {error}', 'msg': str(response['message'])})