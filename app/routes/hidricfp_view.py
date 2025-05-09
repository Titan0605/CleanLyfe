from flask import Blueprint, render_template, redirect, url_for, session

bp = Blueprint("hidricfp_view", __name__)

@bp.route('/hidricfp')
def hidricfp():
    if 'username' in session:
        return render_template('hf_products.html')
    else:
        return redirect(url_for('index_view.index'))