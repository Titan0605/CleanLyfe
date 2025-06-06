from flask import Blueprint, render_template, redirect, url_for, session
import requests

bp = Blueprint("carbonfp_view", __name__)

@bp.route('/carbonfp')
def carbonfp():
    if 'username' in session:
        return render_template('carbonfp.html')
    else:
        return redirect(url_for('index_view.index'))


@bp.route('/carbonfp/transport')
def carbonfp_transport():
    if 'username' in session:
        return render_template('carbonfp_transport.html')
    else:
        return redirect(url_for('index_view.index'))


@bp.route('/carbonfp/devices')
def carbonfp_devices():
    api_get_devices  = "http://127.0.0.1:3000/carbonfp/get-devices"  
    if 'username' in session:   
        response = requests.get(api_get_devices)
        response.raise_for_status()

        devices = response.json()
        return render_template('carbonfp_devices.html') #, devices=devices)
    else:
        return redirect(url_for('index_view.index'))


@bp.route('/carbonfp/products')
def carbonfp_products():
    if 'username' in session:
        return render_template('carbonfp_products.html')
    else:
        return redirect(url_for('index_view.index'))
    
@bp.route('/carbonfp/water')
def carbonfp_water():
    if 'username' in session:
        return render_template('carbonfp_water.html')
    else:
        return redirect(url_for('index_view.index'))