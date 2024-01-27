#routes file for navigating in the app
from app import app
from modules.clothes import get_clothes, add_clothes
from modules.login import register, login, logout
from models import Category, Brand, Size
from flask import render_template

#calls index.html the main page and renders the clothes from database
@app.route("/")
def index():
    return get_clothes()

#renders new.html and adds categories, brands, sizes from database to the select list
@app.route("/new", methods=['GET'])
def new():
    categories = Category.query.all()
    brands = Brand.query.all()
    sizes = Size.query.all()
    print(sizes)
    return render_template('new.html', categories=categories, brands=brands, sizes=sizes)

#adding a new garment
@app.route("/send", methods=["POST"])
def send():
    return add_clothes()

#register a new account
@app.route("/register", methods=["GET", "POST"])
def register_route():
    return register()

#login
@app.route("/login", methods=["GET", "POST"])
def login_route():
    return login()

#logout
@app.route("/logout")
def logout_route():
    return logout()

#about us file
@app.route("/about")
def about():
    return render_template("about.html")

#faq template
@app.route("/faq")
def faq():
    return render_template("faq.html")