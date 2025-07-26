from flask import Blueprint, render_template, redirect, url_for, session

bp = Blueprint("hydricfp_views", __name__)

@bp.route('/hydricfp')
def hydricfp():
    if 'username' in session:
        user = session
        return render_template('hf_products.html', user=user)
    else:
       return redirect(url_for('indexes_views.index_views'))