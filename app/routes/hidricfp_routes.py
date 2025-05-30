from flask import Blueprint, Response, render_template, redirect, url_for, request, jsonify
from app.services.water_products_calculus import HidricCalculator, calculate_consumption
from app.models.hidric_products_model import Hidcric_products_model

bp = Blueprint("hidricfp_routes", __name__)

@bp.route('/hidricfp/calculation', methods=['POST'])
def calculate_hidric_footprint() -> Response:
    calculator = HidricCalculator()
    hidric_model = Hidcric_products_model()
    try:
        data = request.get_json()
        print(data)
        
        total_consumption: int = calculate_consumption(calculator, data)
        
        print(total_consumption)
        
        response = hidric_model.insert_consumption(total_consumption)
    
        render_template("home.html")
        return jsonify({'status': 'Data saved in DB', 'msg': response})
    except ValueError as error:
        return jsonify({'status': f'Invalid value: {error}', 'msg': response})