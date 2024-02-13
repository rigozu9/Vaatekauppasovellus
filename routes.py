#routes file for navigating in the app
from app import app
from modules.clothes import get_categories_and_brands, add_clothes, get_clothes_by_category, get_clothes_by_brand, get_clothes_by_id, get_clothes_by_search
from modules.login import register, login, logout
from modules.user import get_clothes_by_user
from models import Category, Brand, Size
from flask import render_template

#For the picture to render from the database need to 
#define a custom Jinja2 filter for base64 encoding
import base64

@app.template_filter('b64encode')
def b64encode_filter(data):
    return base64.b64encode(data).decode('utf-8')

#calls index.html the main page and renders the categories and brands from database
@app.route("/")
def index():
    return get_categories_and_brands()

#calls category.html the category page and renders the clothes from selected category from database
@app.route('/category/<category_name>')
def category(category_name):
    return get_clothes_by_category(category_name)

#calls category.html the category page and renders the clothes from selected category from database
@app.route('/brands/<brand_name>')
def brand(brand_name):
    return get_clothes_by_brand(brand_name)

#calls garment.html
@app.route('/garment/<garment_id>')
def garment(garment_id):
    return get_clothes_by_id(garment_id)

#route for search
@app.route('/search')
def search():
    return get_clothes_by_search()

#renders new.html and adds categories, brands, sizes from database to the select list
@app.route("/new", methods=['GET'])
def new():
    categories = Category.query.all()
    brands = Brand.query.all()
    sizes = Size.query.all()
    return render_template('new.html', categories=categories, brands=brands, sizes=sizes)

#calls usertab.html where usertab renders and shows own listings
@app.route('/users/<user_name>')
def user_tab(user_name):
    return get_clothes_by_user(user_name)

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
@app.route("/FAQ")
def faq():
    return render_template("faq.html")