from flask import redirect, render_template, request, session
from db import db
from models import Clothing
import os
from werkzeug.utils import secure_filename

# Where the pictures are uploaded
UPLOAD_FOLDER = 'static/uploads' 
# Check if the filename has an allowed extension
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Method to get clothes from the database
def get_clothes():
    result = Clothing.query.all()
    return render_template("index.html", result=result)

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
