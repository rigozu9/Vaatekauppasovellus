from app import app
import clothes
from db import db
from flask import redirect, render_template, request, session
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy.sql import text

#Get all clothes
@app.route("/")
def index():
    result = clothes.get_clothes()  # Correctly assign the result
    return render_template("index.html", result=result)

#Sell a garment
@app.route("/new")
def new():
    return render_template("new.html")

@app.route("/send", methods=["POST"])
def send():
    content = request.form["content"]
    sql = text("INSERT INTO clothes (name) VALUES (:name)")
    db.session.execute(sql, {"name":content})
    db.session.commit()
    return redirect("/")

#Account registeration. Sends username and hashed password into the database
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        hash_value = generate_password_hash(password)
        sql = text("INSERT INTO users (username, password) VALUES (:username, :password)")
        db.session.execute(sql, {"username": username, "password": hash_value})
        db.session.commit()
        session["username"] = username
        return redirect("/")
    return render_template("register.html")

#Account login check if credentials are correct
@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]

    sql = text("SELECT id, password FROM users WHERE username=:username")
    result = db.session.execute(sql, {"username": username})
    user = result.fetchone()

    if not user:
        return render_template("login.html", error="Invalid username or password")
    hash_value = user.password

    if check_password_hash(hash_value, password):
        session["username"] = username
        return redirect("/")
    else:
        return render_template("login.html", error="Invalid username or password")

#Log out
@app.route("/logout")
def logout():
    del session["username"]
    return redirect("/")