from flask import Flask, Blueprint, render_template, redirect, url_for, session

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
    if 'username' in session:
        return render_template('carbonfp_devices.html')
    else:
        return redirect(url_for('index_view.index'))