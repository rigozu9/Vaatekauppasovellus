#routes file for navigating in the app
from app import app
from sqlalchemy import and_, or_, desc
from modules.clothes import (
    get_categories_and_brands,
    add_clothes,
    get_clothes_by_category,
    get_clothes_by_brand,
    get_clothes_by_id,
    get_clothes_by_search,
    delete_garment,
    modify_garment,
)
from modules.messages import send_message, get_messages
from modules.login import register, login, logout
from modules.user import (
    get_info_by_user, 
    buy_clothing,
    get_chats,
    add_balance
)
from models import (
    Category, 
    Brand, 
    Size, 
    Clothing, 
    Image, 
    Message, 
    Chat,
    User
)
from flask import render_template, request, session

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

#calls garmentpage.html
@app.route('/garment/<garment_id>')
def garment(garment_id):
    return get_clothes_by_id(garment_id)

#Route to add balance
@app.route('/balance/<username>', methods=['GET', 'POST'])
def balance(username):
    user = User.query.filter_by(username=session.get('username')).first()
    if request.method == "POST":
        return add_balance()
    else: 
        return render_template("balance.html", user=user)

#route for buying item
@app.route('/buy/<garment_id>')
def buy_item(garment_id):
    return buy_clothing(garment_id)

#route for search
@app.route('/search')
def search():
    return get_clothes_by_search()

#renders new.html and adds categories, brands, sizes from database to the select list
@app.route("/new", methods=["POST", "GET"])
def new():
    categories = Category.query.all()
    brands = Brand.query.all()
    sizes = Size.query.all()
    if request.method == "POST":
        return add_clothes()
    else: 
        return render_template("new.html", categories=categories, brands=brands, sizes=sizes)

#modify a garment if its a get method loads modify_item.html if post if calls modify_garment function 
@app.route("/modify/<garment_id>", methods=["GET", "POST"])
def modify_item(garment_id):
    garment = Clothing.query.get(garment_id)
    categories = Category.query.all()
    brands = Brand.query.all()
    sizes = Size.query.all()
    images = Image.query.all()
    if request.method == "POST":
        return modify_garment(garment_id)
    else:
        return render_template('modify_item.html', garment=garment, categories=categories, brands=brands, sizes=sizes, images=images)

#delete a garmnet
@app.route("/delete/<garment_id>")
def delete_item(garment_id):
    return delete_garment(garment_id)

#if GET renders item_messages.html tempalte if POST sends message by calling the function send_message 
@app.route('/send_message/<sender_username>/<receiver_username>/<garment_id>', methods=['GET', 'POST'])
def user_send_message(sender_username, receiver_username, garment_id):    
    if request.method == 'POST':
        return send_message()
    else:
        return get_messages(sender_username, receiver_username, garment_id)

        
#Route for users to check inquiries on their listings
@app.route('/chats/<seller_username>/<garment_id>', methods=['GET', 'POST'])
def user_get_chats(seller_username, garment_id):
    return get_chats(seller_username, garment_id)

#calls usertab.html where usertab renders and shows own listings
@app.route('/users/<user_name>')
def user_tab(user_name):
    return get_info_by_user(user_name)

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