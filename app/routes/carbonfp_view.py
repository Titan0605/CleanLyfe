from flask import Flask, Blueprint, render_template, redirect, url_for, session
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
    # kitchen_devices  = "http://127.0.0.1:3000/carbonfp/get-devices-location/Kitchen"
    # living_devices  = "http://127.0.0.1:3000/carbonfp/get-devices-location/Kitchen"
    # bedroom_devices  = "http://127.0.0.1:3000/carbonfp/get-devices-location/Kitchen"
    # office_devices  = "http://127.0.0.1:3000/carbonfp/get-devices-location/Kitchen"
    # bathroom_devices  = "http://127.0.0.1:3000/carbonfp/get-devices-location/Kitchen"
    # laundry_devices  = "http://127.0.0.1:3000/carbonfp/get-devices-location/Kitchen"
    # mobile_devices  = "http://127.0.0.1:3000/carbonfp/get-devices-location/Kitchen"
    # others_devices  = "http://127.0.0.1:3000/carbonfp/get-devices-location/Kitchen"

    
        api_get_devices  = "http://127.0.0.1:3000/carbonfp/get-devices"  
        if 'username' in session:   
            response = requests.get(api_get_devices)
            response.raise_for_status()

            devices = response.json()
            return render_template('carbonfp_devices.html', devices=devices)
        else:
            return redirect(url_for('index_view.index'))
    