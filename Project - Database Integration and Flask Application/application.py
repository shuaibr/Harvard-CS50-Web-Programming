from wtforms.validators import DataRequired, Length
from wtforms import StringField, TextField, SubmitField
from flask_wtf import Form
import xml.etree.ElementTree as ET
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy import create_engine
from flask_session import Session
from flask import Flask, redirect, url_for,  session, session, g, request, render_template, request, flash
import os
import psycopg2
import requests
import gc
from wtforms import Form, BooleanField, StringField, PasswordField, validators

res = requests.get("https://www.goodreads.com/book/review_counts.json",
                   params={"key": "BgzQ9doaTztk9S8YBTVefg", "isbns": "9781632168146"})


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

SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY


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


class Login(Form):
    username = TextField(
        'Username', [validators.Length(min=4, max=20)])
    password = PasswordField(
        'Password', [validators.Required()])


@app.route("/login", methods=["GET", "POST"])
def login():
    try:

        print("Trying: !!! ")
        msg = "Log in to access your account"
        print("Requesting form")
        form = Login(request.form)
        username = form.username.data
        password = form.password.data
        print("requested, gettingDB")
        conn = psycopg2.connect(
            "host=ec2-52-207-25-133.compute-1.amazonaws.com dbname=    dc4ua1h8pt5m05 user=pxondfbtekevjh password=eb9a343232a10bb904c71b3c94669edcaad8f15e77796d4e9f47543b885ed875")
        print("conn established")
        cur = conn.cursor()
        print("dB connected")

        if request.method == "POST" and form.validate():
            data = cur.execute(
                "SELECT * FROM users WHERE username = '{0}'".format(username))
            check = cur.fetchone()
            print("login check: ", check)
            if int(len(check)) == 0:
                return render_template("registration.html", form=form, error_message="Register before loggin in!")
            elif check[2] == password:
                print("success!")
                session['logged_in'] = True
                session['username'] = username

                flash("You are now loggin in")
                return redirect(url_for('index'))
            else:
                print("invalid password!")
                msg = "Invalid password, try again!"

            cur.close()
            conn.close()
            gc.collect()

        return render_template("login.html", form=form, msg=msg)

    except Exception as e:
        return (str(e))


class Register(Form):
    username = TextField(
        'Username', [validators.Length(min=4, max=20)])
    password = PasswordField(
        'Password', [validators.Required(), validators.EqualTo('confirm', message="Passwords must match!")])
    confirm = PasswordField(
        'Repeat Password')


@app.route("/registration", methods=["GET", "POST"])
def registration():
    try:
        form = Register(request.form)
        if request.method == "POST" and form.validate():
            print("Connecting to DB1!")
            username = form.username.data
            password = form.password.data

            conn = psycopg2.connect(
                "host=ec2-52-207-25-133.compute-1.amazonaws.com dbname=    dc4ua1h8pt5m05 user=pxondfbtekevjh password=eb9a343232a10bb904c71b3c94669edcaad8f15e77796d4e9f47543b885ed875")
            cur = conn.cursor()
            print("Connected, attempting to query username")
            x = cur.execute(
                "SELECT * FROM users WHERE username = '{0}'".format(username))
            # print("username exists check: ", x, cur.fetchall())
            check = cur.fetchall()
            if int(len(check)) > 0:
                return render_template("registration.html", form=form, error_message="Username already exsits, please choose another!")
            else:
                cur.execute(
                    "INSERT INTO users  (username, password) VALUES ('{0}','{1}')".format(username, password))
                conn.commit()

                flash("Thank you for registering!")
                cur.close()
                conn.close()
                gc.collect()

                session['logged_in'] = True
                session['username'] = username

                return redirect(url_for('index'))
        return render_template("registration.html", form=form, error_message="Register today!")

    except Exception as e:
        print("ERROR EXCEPTION")
        return (str(e))


@app.route("/search", methods=["GET", "POST"])
def search():
    search = request.form.get("search")

    res = requests.get(" https://www.goodreads.com/search/index.xml",
                       params={"key": "BgzQ9doaTztk9S8YBTVefg", "q": str(search)})
    tree = res.content
    # print("\n", tree, "\n")
    root = ET.fromstring(tree)
    books_array = []
    # print(root[1][6].tag, " ", root[1][6].text)
    result = root[1][6]
    for child in result.iter("work"):
        isbn = 0
        book = child.find('best_book')
        author = book.find('author')[1].text
        title = book.find('title').text
        pub_year = child.find('original_publication_year').text
        goodreads_id = book.find('id').text
        # isbn_res = requests.get("https://www.goodreads.com/book/show.xml", params={
        #                         "key": "BgzQ9doaTztk9S8YBTVefg", "id": str(goodreads_id)})
        # iroot = ET.fromstring(isbn_res.content)
        # isbn = iroot[1][3].text
        # # print("ISBN: ", isbn)

        # # print(author, title, pub_year, isbn)
        books_array.append([author, title, pub_year, goodreads_id])

    # print("books array: ", books_array)
    return render_template("/search.html", search=search, results=books_array)


@app.route("/bookpage", methods=["GET", "POST"])
def bookpage():
    info = request.form.get("info")
    print("INFO ID: ", info)
    isbn = 0
    result = 0
    isbn_res = requests.get("https://www.goodreads.com/book/show.xml", params={
                            "key": "BgzQ9doaTztk9S8YBTVefg", "id": str(info)})
    iroot = ET.fromstring(isbn_res.content)
    isbn = iroot[1][3].text
    title = iroot[1][1].text
    pub_year = iroot[1][10].text
    author = iroot[1][26][0][1].text
    num_ratings = iroot[1][22].text
    avg_ratings = iroot[1][18].text
    img = iroot[1][8].text

    result = [author, title, pub_year, isbn, num_ratings, avg_ratings, img]
    print("RESULT: ", result)

    return render_template("/bookpage.html", search=search, book_info=result)
