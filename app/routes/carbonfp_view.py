from flask import Blueprint, render_template, redirect, url_for, session
from app.models.carbon_energy_model import ElectricDevicesModel

bp = Blueprint("carbonfp_view", __name__)

@bp.route('/carbonfp')
def carbonfp():
    #if 'username' in session:
        return render_template('carbonfp.html')
    #else:
     #   return redirect(url_for('index_view.index'))


@bp.route('/carbonfp/transport')
def carbonfp_transport():
    #if 'username' in session:
        return render_template('carbonfp_transport.html')
    #else:
     #   return redirect(url_for('index_view.index'))


@bp.route('/carbonfp/energy')
def carbonfp_devices():
    #if 'username' in session:  
    energy_model = ElectricDevicesModel()

    devices = energy_model.get_all_devices()
    return render_template('carbonfp_energy.html', devices=devices)
    #else:
   #     return redirect(url_for('index_view.index'))


@bp.route('/carbonfp/products')
def carbonfp_products():
    #if 'username' in session:
        return render_template('carbonfp_products.html')
    #else:
    #    return redirect(url_for('index_view.index'))
    
@bp.route('/carbonfp/water')
def carbonfp_water():
    #if 'username' in session:
        return render_template('carbonfp_water.html')
    #else:
    #    return redirect(url_for('index_view.index'))