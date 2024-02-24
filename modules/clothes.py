from flask import redirect, render_template, request, session
from db import db
import base64
from sqlalchemy import text
from models import Clothing, Image

# Check if the filename has an allowed extension
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Method to get categories and brands from the database
def get_categories_and_brands():
    categories_query = text("SELECT * FROM categories")
    brands_query = text("SELECT * FROM brands")

    categories = db.session.execute(categories_query).fetchall()
    brands = db.session.execute(brands_query).fetchall()

    if 'username' in session:
        user_query = text("SELECT * FROM users WHERE username = :username")
        user = db.session.execute(user_query, {"username": session['username']}).fetchone()
        return render_template("index.html", categories=categories, brands=brands, user=user)
    else:
        return render_template("index.html", categories=categories, brands=brands)

# Method to get clothes based on category from the database
def get_clothes_by_category(category_name):
    clothes_query = text("""
        SELECT c.*, i.data AS image_data
        FROM clothes c
        LEFT JOIN (
            SELECT clothing_id, data,
                   ROW_NUMBER() OVER (PARTITION BY clothing_id ORDER BY id) AS rn
            FROM images
        ) i ON c.id = i.clothing_id AND i.rn = 1
        WHERE c.category = :category
    """)
    clothes = db.session.execute(clothes_query, {"category": category_name}).fetchall()

    if 'username' in session:
        # Retrieve user information
        user_query = text("SELECT * FROM users WHERE username = :username")
        user = db.session.execute(user_query, {"username": session['username']}).fetchone()
        return render_template("category.html", clothes=clothes, category_name=category_name, user=user) 
    else:
        return render_template("category.html", clothes=clothes, category_name=category_name)



# Method to get clothes based on brands from the database
def get_clothes_by_brand(brand_name):
    if brand_name != "All brands":
        clothes_query = text("""
            SELECT c.*, i.data AS image_data
            FROM clothes c
            LEFT JOIN (
                SELECT DISTINCT ON (clothing_id) clothing_id, data
                FROM images
            ) i ON c.id = i.clothing_id
            WHERE c.brand = :brand_name
        """)
        clothes = db.session.execute(clothes_query, {"brand_name": brand_name}).fetchall()

        if 'username' in session:
            user_query = text("SELECT * FROM users WHERE username = :username")
            user = db.session.execute(user_query, {"username": session['username']}).fetchone()
            return render_template("category.html", clothes=clothes, brand_name=brand_name, user=user)
        else:
            return render_template("category.html", clothes=clothes, brand_name=brand_name)
    else:
        clothes_query = text("""
            SELECT c.*, i.data AS image_data
            FROM clothes c
            LEFT JOIN (
                SELECT DISTINCT ON (clothing_id) clothing_id, data
                FROM images
            ) i ON c.id = i.clothing_id
        """)
        clothes = db.session.execute(clothes_query).fetchall()

        if 'username' in session:
            user_query = text("SELECT * FROM users WHERE username = :username")
            user = db.session.execute(user_query, {"username": session['username']}).fetchone()
            return render_template("category.html", clothes=clothes, brand_name="All brands", user=user)
        else:
            return render_template("category.html", clothes=clothes, brand_name="All brands")

# Method to get clothes based on search
def get_clothes_by_search():
    query = request.args.get('query') # Get the search query from the request
    clothes_query = text("""
        SELECT c.*, i.data AS image_data
        FROM clothes c
        LEFT JOIN (
            SELECT DISTINCT ON (clothing_id) clothing_id, data
            FROM images
        ) i ON c.id = i.clothing_id
        WHERE c.name ILIKE :query
    """)
    clothes = db.session.execute(clothes_query, {"query": f'%{query}%'}).fetchall()

    if 'username' in session:
        user_query = text("SELECT * FROM users WHERE username = :username")
        user = db.session.execute(user_query, {"username": session['username']}).fetchone()
        return render_template("category.html", clothes=clothes, query=query, user=user)
    else:
        return render_template("category.html", clothes=clothes, query=query)

# Method to get clothes based on ID from the database
def get_clothes_by_id(garment_id):
    # Fetch clothing information
    clothing_query = text("""
        SELECT *
        FROM clothes
        WHERE id = :garment_id
    """)
    clothing_result = db.session.execute(clothing_query, {"garment_id": garment_id}).fetchone()

    # Fetch images associated with the clothing item
    images_query = text("""
        SELECT data
        FROM images
        WHERE clothing_id = :garment_id
    """)
    images_result = db.session.execute(images_query, {"garment_id": garment_id}).fetchall()

    # Convert image data to a list
    image_data_list = [row[0] for row in images_result]

    admin_query = text("SELECT * FROM users WHERE role = 'admin'")
    admin = db.session.execute(admin_query).fetchone()

    if 'username' in session:
        user_query = text("SELECT * FROM users WHERE username = :username")
        user = db.session.execute(user_query, {"username": session['username']}).fetchone()
        return render_template("garmentpage.html", clothing=clothing_result, images=image_data_list, admin=admin, user=user)
    else:
        return render_template("garmentpage.html", clothing=clothing_result, images=image_data_list, admin=admin)

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

    # Add new clothing item
    add_clothes_query = text("""
        INSERT INTO clothes (name, description, category, brand, size, price, username)
        VALUES (:name, :description, :category, :brand, :size, :price, :username)
        RETURNING id
    """)
    result = db.session.execute(add_clothes_query, {
        "name": name,
        "description": description,
        "category": category,
        "brand": brand,
        "size": size,
        "price": price,
        "username": username
    })
    new_clothes_id = result.fetchone()[0]

    # Add images for the new clothing item
    for file in files:
        if file and allowed_file(file.filename):
            image_data = file.read()
            add_image_query = text("""
                INSERT INTO images (clothing_id, data)
                VALUES (:clothing_id, :data)
            """)
            db.session.execute(add_image_query, {"clothing_id": new_clothes_id, "data": image_data})

    db.session.commit()
    return redirect("/")

# Added function to delete garment. Redirects to usertab
def delete_garment(garment_id):
    username = session['username']
    
    # Construct a text-based query to delete the garment by ID
    delete_query = text("DELETE FROM clothes WHERE id = :garment_id")
    
    # Execute the query with the garment_id parameter
    db.session.execute(delete_query, {"garment_id": garment_id})
    db.session.commit()

    return redirect(f"/users/{username}")

# Function to modify items
def modify_garment(garment_id):
    # Get the username from the session
    username = session['username']
    
    # Get the form data from the request
    name = request.form['name']
    description = request.form['description']
    brand = request.form['brand']
    category = request.form['category']
    size = request.form['size']
    price = request.form['price']
    
    # Update the garment attributes with the new data
    update_query = text("""
        UPDATE clothes
        SET name = :name, description = :description, brand = :brand,
            category = :category, size = :size, price = :price
        WHERE id = :garment_id
    """)
    db.session.execute(update_query, {
        "name": name,
        "description": description,
        "brand": brand,
        "category": category,
        "size": size,
        "price": price,
        "garment_id": garment_id
    })

    # Handle image upload
    if 'image' in request.files:
        files = request.files.getlist('image')  # Retrieve multiple files

        # Delete existing images associated with the garment
        delete_images_query = text("""
            DELETE FROM images
            WHERE clothing_id = :garment_id
        """)
        db.session.execute(delete_images_query, {"garment_id": garment_id})

        # Insert new images for the garment
        for file in files:
            if file and allowed_file(file.filename):
                image_data = file.read()
                add_image_query = text("""
                    INSERT INTO images (clothing_id, data)
                    VALUES (:clothing_id, :data)
                """)
                db.session.execute(add_image_query, {"clothing_id": garment_id, "data": image_data})

    # Commit changes to the database
    db.session.commit()

    # Redirect to the user's profile page
    return redirect(f"/users/{username}")
