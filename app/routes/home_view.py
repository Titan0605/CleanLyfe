from flask import Flask, render_template, Blueprint

bp = Blueprint("home_view", __name__)

@bp.route("/home/<int:id>")
def home(id):
    return render_template("home.html")