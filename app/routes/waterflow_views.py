from flask import Blueprint, render_template

bp = Blueprint("waterflow_routes", __name__)

@bp.route('/waterflow')
def waterFlow_service():
    return render_template('waterflow_index.html')
