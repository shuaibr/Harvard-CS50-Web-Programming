from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy import create_engine
from flask_session import Session
from flask import Flask, session, render_template, request
import os
import requests
res = requests.get("https://www.goodreads.com/book/review_counts.json",
                   params={"key": "BgzQ9doaTztk9S8YBTVefg", "isbns": "9781632168146"})
print(res.json())


app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html")


@app.route("/thoughts")
def thoughts():
    return render_template("thoughts.html")


@app.route("/portfolio")
def portfolio():
    return render_template("portfolio.html")


@app.route("/books")
def books():
    return render_template("/books.html")


@app.route("/login")
def login():
    return render_template("/login.html")


@app.route("/registration")
def registration():
    return render_template("/registration.html")


@app.route("/bookpage", methods=["GET", "POST"])
def bookpage():
    search = request.form.get("search")
    res = requests.get("https://www.goodreads.com/book/review_counts.json",
                       params={"key": "BgzQ9doaTztk9S8YBTVefg", "isbns": str(search)})
    return render_template("/bookpage.html", search=search, result=res.json())
