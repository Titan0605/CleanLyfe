from flask import render_template, Blueprint

bp = Blueprint("index_view", __name__)

@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/sign_up_view')
def sign_up():
    return render_template('sign_up.html')

@bp.route('/login')
def login():
    return render_template('login.html')