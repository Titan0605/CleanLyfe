from flask import render_template, Blueprint, url_for

bp = Blueprint("index_views", __name__)

@bp.route('/')
def index_views():
    return render_template("index_worldmatters.html")