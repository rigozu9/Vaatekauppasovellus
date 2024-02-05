#module for user related functions
from flask import render_template
from models import Clothing

# Method to get clothes that the "username" listed
def get_clothes_by_user(username):
    clothes = Clothing.query.filter_by(username=username).all()
    print(clothes)
    return render_template("usertab.html", clothes=clothes)
