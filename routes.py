#routes call functions from clothes.py and login.py
from app import app
from clothes import get_clothes, add_clothes
from login import register, login, logout
from flask import render_template

@app.route("/")
def index():
    return get_clothes()

#Render new template where you can add a new garment for sale 
@app.route("/new")
def new():
    return render_template("new.html")

@app.route("/send", methods=["POST"])
def send():
    return add_clothes()

@app.route("/register", methods=["GET", "POST"])
def register_route():
    return register()

@app.route("/login", methods=["POST"])
def login_route():
    return login()

@app.route("/logout")
def logout_route():
    return logout()

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/faq")
def faq():
    return render_template("faq.html")