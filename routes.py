#routes file for navigating in the app
from app import app
from sqlalchemy import text
from db import db
from modules.clothes import (
    get_clothes,
    add_clothes,
    get_clothes_by_category,
    get_clothes_by_brand,
    get_clothes_by_id,
    get_clothes_by_search,
    delete_garment,
    modify_garment,
    admin_pick
)
from modules.messages import send_message, get_messages
from modules.login import register, login, logout
from modules.user import (
    get_info_by_user, 
    buy_clothing,
    get_chats,
    add_balance,
)
from flask import render_template, request, session, jsonify

#For the picture to render from the database need to 
#define a custom Jinja2 filter for base64 encoding
import base64

@app.template_filter('b64encode')
def b64encode_filter(data):
    return base64.b64encode(data).decode('utf-8')

#calls index.html the main page and renders the categories and brands from database
@app.route("/")
def index():
    return get_clothes()

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
    # Define the SQL query using text
    sql_query = text("SELECT * FROM users WHERE username = :username")

    # Execute the SQL query with parameters
    result = db.session.execute(sql_query, {"username": session.get('username')})

    # Fetch the first row from the result
    user = result.fetchone()

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

@app.route("/new", methods=["POST", "GET"])
def new():
    categories_query = text("SELECT * FROM categories")
    brands_query = text("SELECT * FROM brands")
    sizes_query = text("SELECT * FROM sizes")

    # Execute the raw SQL queries
    categories = db.session.execute(categories_query).fetchall()
    brands = db.session.execute(brands_query).fetchall()
    sizes = db.session.execute(sizes_query).fetchall()

    if request.method == "POST":
        return add_clothes()
    else: 
        return render_template("new.html", categories=categories, brands=brands, sizes=sizes)
    
#in new.html subcategories render based on main category
@app.route("/get-subcategories")
def get_subcategories():
    category_id = request.args.get('category_id')
    subcategories_query = text("SELECT * FROM subcategories WHERE category_id = :category_id")
    subcategories = db.session.execute(subcategories_query, {'category_id': category_id}).fetchall()
    # Convert subcategories to a list of dicts
    subcategories_list = [{'id': sub.id, 'name': sub.name} for sub in subcategories]
    return jsonify(subcategories_list)

#in new.html sizes render based on main category
@app.route("/get-sizes")
def get_sizes():
    category_id = request.args.get('category_id')
    size_query = text("""
        SELECT s.id, s.name FROM sizes s
        JOIN category_sizes cs ON s.id = cs.size_id
        WHERE cs.category_id = :category_id
    """)
    sizes = db.session.execute(size_query, {'category_id': category_id}).fetchall()
    sizes_list = [{'id': size.id, 'name': size.name} for size in sizes]
    return jsonify(sizes_list)


    
#route to search for existing brands from database when adding a newlisting
@app.route('/search-brand')
def search_brand():
    query = request.args.get('query', '')
    if query:
        # Raw SQL query to search for brands that match the query
        search_query = text("SELECT name FROM brands WHERE name ILIKE :query")
        result = db.session.execute(search_query, {'query': f'%{query}%'}).fetchall()
        # Convert result to a list of brand names
        brand_names = [row[0] for row in result]
        return jsonify(brand_names)
    return jsonify([])

@app.route("/modify/<garment_id>", methods=["GET", "POST"])
def modify_item(garment_id):
    garment_query = text("SELECT * FROM clothes WHERE id = :garment_id")
    categories_query = text("SELECT * FROM categories")
    brands_query = text("SELECT * FROM brands")
    sizes_query = text("SELECT * FROM sizes")
    images_query = text("SELECT * FROM images WHERE clothing_id = :garment_id")

    garment = db.session.execute(garment_query, {"garment_id": garment_id}).fetchone()
    categories = db.session.execute(categories_query).fetchall()
    brands = db.session.execute(brands_query).fetchall()
    sizes = db.session.execute(sizes_query).fetchall()
    images = db.session.execute(images_query, {"garment_id": garment_id}).fetchall()

    if request.method == "POST":
        return modify_garment(garment_id)
    else:
        return render_template('modify_item.html', garment=garment, categories=categories, brands=brands, sizes=sizes, images=images)

#delete a garmnet
@app.route("/delete/<garment_id>")
def delete_item(garment_id):
    return delete_garment(garment_id)

#delete a garmnet
@app.route("/admin_pick/<garment_id>")
def adminpick(garment_id):
    return admin_pick(garment_id)

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