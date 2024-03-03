from flask import redirect, render_template, request, session, flash
from db import db
from sqlalchemy import text
from sqlalchemy.exc import DataError
from decimal import Decimal

# Check if the filename has an allowed extension
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Method to get categories and brands from the database
def get_clothes():
    clothes_query = text("""
        SELECT c.*, i.data AS image_data
        FROM clothes c
        LEFT JOIN (
            SELECT clothing_id, data,
                   ROW_NUMBER() OVER (PARTITION BY clothing_id ORDER BY main_image DESC, id) AS rn  
            FROM images
        ) i ON c.id = i.clothing_id AND i.rn = 1
    """)
    categories_query = text("SELECT * FROM categories")
    brands_query = text("SELECT * FROM brands WHERE name IN ('NUMBER (N)INE', 'BAPE', 'junya watanabe', 'All brands')")

    clothes = db.session.execute(clothes_query).fetchall()
    categories = db.session.execute(categories_query).fetchall()
    brands = db.session.execute(brands_query).fetchall()

    if 'username' in session:
        user_query = text("SELECT * FROM users WHERE username = :username")
        user = db.session.execute(user_query, {"username": session['username']}).fetchone()
        return render_template("index.html", clothes=clothes, categories=categories, brands=brands, user=user)
    else:
        return render_template("index.html", clothes=clothes, categories=categories, brands=brands)

def get_clothes_by_category(category_name):
    clothes_query = text("""
        SELECT c.*, i.data AS image_data
        FROM clothes c
        LEFT JOIN (
            SELECT clothing_id, data,
                   ROW_NUMBER() OVER (PARTITION BY clothing_id ORDER BY main_image DESC, id) AS rn  
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
                SELECT clothing_id, data,
                    ROW_NUMBER() OVER (PARTITION BY clothing_id ORDER BY main_image DESC, id) AS rn  
                FROM images
            ) i ON c.id = i.clothing_id AND i.rn = 1
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
                SELECT clothing_id, data,
                    ROW_NUMBER() OVER (PARTITION BY clothing_id ORDER BY main_image DESC, id) AS rn  
                FROM images
            ) i ON c.id = i.clothing_id AND i.rn = 1
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
            SELECT clothing_id, data,
                ROW_NUMBER() OVER (PARTITION BY clothing_id ORDER BY main_image DESC, id) AS rn  
            FROM images
        ) i ON c.id = i.clothing_id AND i.rn = 1
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
        ORDER BY main_image DESC, id
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


# Validate price function
def is_valid_price(price):
    try:
        price_value = Decimal(price)
        return price_value > 0
    except:
        return False

# Add new clothes
def add_clothes():
    name = request.form["name"]
    description = request.form["description"]
    category_id = request.form["category"]
    subcategory = request.form["subcategory"]
    brand = request.form["brand"]
    size = request.form["size"]
    price = request.form["price"]
    
    category_name_query = text("SELECT name FROM categories WHERE id = :category_id")
    category_name_result = db.session.execute(category_name_query, {"category_id": category_id})
    category_name_row = category_name_result.fetchone()

    # Extract the category name from the result
    if category_name_row:
        category_name = category_name_row[0]
    else:
        # Handle case where category ID does not exist
        return "Category not found", 400

    if 'username' in session:
        username = session['username']

    if 'image' in request.files:
        files = request.files.getlist('image')  # Retrieve multiple files

    # Check if brand exists, if not, add it
    brand_exists_query = text("SELECT id FROM brands WHERE name = :brand")
    brand_result = db.session.execute(brand_exists_query, {"brand": brand})
    brand_row = brand_result.fetchone()

    if not brand_row:
        # Add new brand to brands table
        add_brand_query = text("INSERT INTO brands (name) VALUES (:brand)")
        db.session.execute(add_brand_query, {"brand": brand})

    # Add new clothing item
    add_clothes_query = text("""
        INSERT INTO clothes (name, description, category, brand, size, price, username, subcategory)
        VALUES (:name, :description, :category, :brand, :size, :price, :username, :subcategory)
        RETURNING id
    """)
    result = db.session.execute(add_clothes_query, {
        "name": name,
        "description": description,
        "category": category_name,
        "brand": brand,
        "size": size,
        "price": price,
        "username": username,
        "subcategory": subcategory
    })
    
    new_clothes_id = result.fetchone()[0]

    # Initialize main_image_index to None
    main_image_index = None

    # Get the index of the main image, if provided and valid
    if 'main_image_index' in request.form and request.form['main_image_index'].isdigit():
        main_image_index = int(request.form['main_image_index'])

    for index, file in enumerate(files):
        if file and allowed_file(file.filename):
            image_data = file.read()
            # Check if this file's index matches the main image index provided by the user
            # Or if no main image was provided, default to the first image as the main image
            is_main_image = (main_image_index is None and index == 0) or (main_image_index == index)

            add_image_query = text("""
                INSERT INTO images (clothing_id, data, main_image)
                VALUES (:clothing_id, :data, :main_image)
            """)
            db.session.execute(add_image_query, {
                "clothing_id": new_clothes_id,
                "data": image_data,
                "main_image": is_main_image
            })

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
    category_id = request.form['category']
    size = request.form['size']
    price = request.form['price']
    subcategory = request.form['subcategory']

    category_name_query = text("SELECT name FROM categories WHERE id = :category_id")
    category_name_result = db.session.execute(category_name_query, {"category_id": category_id})
    category_name_row = category_name_result.fetchone()

    # Extract the category name from the result
    if category_name_row:
        category_name = category_name_row[0]
    else:
        # Handle case where category ID does not exist
        return "Category not found", 400
    
    # Check if brand exists, if not, add it
    brand_exists_query = text("SELECT id FROM brands WHERE name = :brand")
    brand_result = db.session.execute(brand_exists_query, {"brand": brand})
    brand_row = brand_result.fetchone()

    if not brand_row:
        # Add new brand to brands table
        add_brand_query = text("INSERT INTO brands (name) VALUES (:brand)")
        db.session.execute(add_brand_query, {"brand": brand})


    # Update the garment attributes with the new data
    update_query = text("""
        UPDATE clothes
        SET name = :name, description = :description, brand = :brand,
            category = :category, size = :size, price = :price, subcategory = :subcategory
        WHERE id = :garment_id
    """)
    db.session.execute(update_query, {
        "name": name,
        "description": description,
        "brand": brand,
        "category": category_name,
        "size": size,
        "price": price,
        "subcategory" :subcategory,
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

    # Initialize main_image_index to None
    main_image_index = None

    # Get the index of the main image, if provided and valid
    if 'main_image_index' in request.form and request.form['main_image_index'].isdigit():
        main_image_index = int(request.form['main_image_index'])

    for index, file in enumerate(files):
        if file and allowed_file(file.filename):
            image_data = file.read()
            # Check if this file's index matches the main image index provided by the user
            # Or if no main image was provided, default to the first image as the main image
            is_main_image = (main_image_index is None and index == 0) or (main_image_index == index)
            
            add_image_query = text("""
                INSERT INTO images (clothing_id, data, main_image)
                VALUES (:clothing_id, :data, :main_image)
            """)
            db.session.execute(add_image_query, {
                "clothing_id": garment_id,
                "data": image_data,
                "main_image": is_main_image
            })

    # Commit changes to the database
    db.session.commit()

    # Redirect to the user's profile page
    return redirect(f"/users/{username}")


def admin_pick(garment_id):
    # Fetch the current state of admin_pick for the garment
    current_state_query = text("SELECT admin_pick FROM clothes WHERE id = :garment_id")
    current_state_result = db.session.execute(current_state_query, {"garment_id": garment_id}).fetchone()
    
    if current_state_result:
        new_admin_pick_status = not current_state_result[0]  # Toggle the status
        
        # Define the SQL statement to update the admin_pick column based on the toggled status
        update_statement = text("UPDATE clothes SET admin_pick = :new_status WHERE id = :garment_id")
        
        # Execute the SQL statement with the provided garment_id and the new status
        db.session.execute(update_statement, {"garment_id": garment_id, "new_status": new_admin_pick_status})
        
        # Commit the changes to the database
        db.session.commit()
        
        return redirect(f"/garment/{garment_id}")