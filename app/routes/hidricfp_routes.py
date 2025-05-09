from typing import Dict, Any
from flask import Blueprint, Response, render_template, redirect, url_for, request, jsonify
from app.services.water_products_calculus import HidricCalculator, calculate_consumption

bp = Blueprint("hidricfp_routes", __name__)

@bp.route('/hidricfp/calculation', methods=['POST'])
def calculate_hidric_footprint() -> Response:
    calculator = HidricCalculator()
    try:
        data = request.get_json()
        print(data)
        
        total_consumption: int = calculate_consumption(calculator, data)
    
        return jsonify({'status': 'Request received'})
    except ValueError as error:
        return jsonify({'status': f'Invalid value: {error}'})