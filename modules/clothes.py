from flask import redirect, render_template, request, session
from db import db
from models import Clothing, Category, Brand
import os
from werkzeug.utils import secure_filename

# Where the pictures are uploaded
UPLOAD_FOLDER = 'static/uploads' 
# Check if the filename has an allowed extension
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Method to get all clothes from the database
def get_clothes():
    result = Clothing.query.all()
    return render_template("index.html", result=result)

# Method to get categories and brands from the database
def get_categories_and_brands():
    categories = Category.query.all()
    brands = Brand.query.all()
    return render_template("index.html", categories=categories, brands=brands)


# Method to get clothes based on category from the database
def get_clothes_by_category(category_name):
    clothes = Clothing.query.filter_by(category=category_name).all()
    return render_template("category.html", clothes=clothes)

# Method to get clothes based on brands from the database
def get_clothes_by_brand(brand_name):
    clothes = Clothing.query.filter_by(brand=brand_name).all()
    return render_template("category.html", clothes=clothes)

# Add new clothes now able to upload a picture of the garment.
def add_clothes():
    name = request.form["name"]
    description = request.form["description"]
    category = request.form["category"]
    brand = request.form["brand"]
    size = request.form["size"]
    price = request.form["price"]

    if 'username' in session:
        username = session['username']

    # Image uploading handled here 
    if 'image' in request.files:
        file = request.files['image']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER, filename))

    new_clothes = Clothing(name=name, description=description, category=category, brand=brand, size=size, price=price, username=username, image_path=filename)
    db.session.add(new_clothes)
    db.session.commit()
    return redirect("/")
