import datetime
from flask import Flask, render_template, request, session
from flask_session import Session

app = Flask(__name__)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
holidays = ["Eid", "Christmas"]


@app.route("/", methods=["GET", "POST"])
def index():
    now = datetime.datetime.now()
    new_year = now.month == 1 and now.day == 1
    headline = "Hello"
    if request.method == "POST":
        note = request.form.get("holiday")
        holidays.append(note)
    return render_template("index.html", headline=headline, ny=new_year, holi=holidays)


@app.route("/bye")
def bye():
    bye = "Goodbye"
    return render_template("index.html", headline=bye)


@app.route("/more")
def more():
    return render_template("more.html")


@app.route("/portfolio")
def portfolio():
    return render_template("portfolio.html")


@app.route("/<string:name>")
def hi(name):
    name = name.capitalize()
    return f"hi, {name}!"


@app.route("/hello", methods=["POST"])
def hello():
    name = request.form.get("name")
    return render_template("hello.html", name=name)
