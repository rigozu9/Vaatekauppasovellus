# method to get clothes from database

from db import db
from models import Clothes  # Import Clothes model from models module
from flask import redirect, render_template, request, session

def get_clothes():
    # Fetch all clothing items from the clothes table
    result = Clothes.query.all()
    return render_template("index.html", result=result)

def add_clothes():
    name = request.form["name"]
    category = request.form["category"]
    brand = request.form["brand"]
    size = request.form["size"]
    price = request.form["price"]

    # Check if the user is logged in
    if 'username' in session:
        username = session['username']

    new_clothes = Clothes(name=name, category=category, brand=brand, size=size, price=price, user_id=username)
    db.session.add(new_clothes)
    db.session.commit()
    return redirect("/")

    
