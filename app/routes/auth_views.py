from flask import render_template, Blueprint

bp = Blueprint("auth_views", __name__)

@bp.route('/sign_up')
def sign_up():
    return render_template('sign_up.html')


@bp.route('/login')
def login():
    print("Login view")
    return render_template('login.html')