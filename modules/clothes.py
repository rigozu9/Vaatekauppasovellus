from flask import redirect, render_template, request, session
from db import db
from models import Clothing, Category, Brand, Image

# Check if the filename has an allowed extension
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Method to get categories and brands from the database
def get_categories_and_brands():
    categories = Category.query.all()
    brands = Brand.query.all()
    return render_template("index.html", categories=categories, brands=brands)

# Method to get clothes based on category from the database
def get_clothes_by_category(category_name):
    clothes = Clothing.query.filter_by(category=category_name).all()
    return render_template("category.html", clothes=clothes, category_name=category_name)

# Method to get clothes based on brands from the database
def get_clothes_by_brand(brand_name):
    if brand_name != "All brands":
        clothes = Clothing.query.filter_by(brand=brand_name).all()
        return render_template("category.html", clothes=clothes, brand_name=brand_name)
    else:
        return render_template("category.html", clothes=Clothing.query.all(), brand_name="All brands")
    
# Method to get clothes based on search
def get_clothes_by_search():
    query = request.args.get('query') # Get the search query from the request
    # Filter clothes based on the search query
    clothes = Clothing.query.filter(Clothing.name.ilike(f'%{query}%')).all()
    return render_template("category.html", clothes=clothes, query=query)
    
# Method to get clothes based on category from the database
def get_clothes_by_id(garment_id):
    clothing = Clothing.query.filter_by(id=garment_id).all()
    return render_template("garmentpage.html", clothing=clothing)

# Add new clothes
def add_clothes():
    name = request.form["name"]
    description = request.form["description"]
    category = request.form["category"]
    brand = request.form["brand"]
    size = request.form["size"]
    price = request.form["price"]

    if 'username' in session:
        username = session['username']

    if 'image' in request.files:
        files = request.files.getlist('image')  # Retrieve multiple files

    new_clothes = Clothing(name=name, description=description, category=category, brand=brand, size=size, price=price, username=username)

    # Iterate over each image and create Image objects
    for file in files:
        if file and allowed_file(file.filename):
            image_data = file.read()
            new_image = Image(data=image_data)
            new_clothes.images.append(new_image)

    # Add the new clothing item
    db.session.add(new_clothes)
    db.session.commit()

    return redirect("/")
