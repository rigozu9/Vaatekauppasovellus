# method to get clothes from database and add a new garment

from db import db
from models import Clothing
from flask import redirect, render_template, request, session

# Fetch all clothing items from the clothes table
def get_clothes():
    result = Clothing.query.all()
    return render_template("index.html", result=result)

#Adding new clothes on new.html
def add_clothes():
    name = request.form["name"]
    category = request.form["category"]
    brand = request.form["brand"]
    size = request.form["size"]
    price = request.form["price"]

    # Check if the user is logged in
    if 'username' in session:
        username = session['username']

    new_clothes = Clothing(name=name, category=category, brand=brand, size=size, price=price, username=username)
    db.session.add(new_clothes)
    db.session.commit()
    return redirect("/")

    
