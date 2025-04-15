from flask import Flask, render_template, Blueprint, session

bp = Blueprint("home_view", __name__)

@bp.route("/home")
def home():
    return render_template("home.html")