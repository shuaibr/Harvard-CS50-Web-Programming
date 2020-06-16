import os

from flask import Flask, redirect, url_for,  session, g, request, render_template, request, flash
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
socketio = SocketIO(app)


@app.route("/", methods=["GET", "POST"])
def login():
    user = request.form.get("username")
    if user == None:
        return render_template("login.html")
    else:
        return render_template("home.html", user=user)


@app.route("/home", methods=["GET", "POST"])
def index():
    user = request.form.get("username")
    print(user)
    return render_template("home.html", user=user)
