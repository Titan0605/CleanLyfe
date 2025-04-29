from flask import Flask, render_template, redirect, url_for, Blueprint, session

bp = Blueprint("home_view", __name__)

@bp.route("/home")
def home():
    if "username" in session:
        user = session
        return render_template("home.html", user=user)
    else:
        return redirect(url_for('index_view.index'))