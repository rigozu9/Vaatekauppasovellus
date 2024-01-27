# method to get clothes from database

from db import db
from models import Clothes  # Import Clothes model from models module
from flask import redirect, render_template, request

def get_clothes():
    # Fetch all clothing items from the clothes table
    result = Clothes.query.all()
    return render_template("index.html", result=result)

def add_clothes():
    content = request.form["content"]
    new_clothes = Clothes(name=content)
    db.session.add(new_clothes)
    db.session.commit()
    return redirect("/")
    
