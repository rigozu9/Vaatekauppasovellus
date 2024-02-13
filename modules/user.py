#module for user related functions
from flask import render_template
from models import Clothing

# Method to get clothes that the "username" listed
#Imports username aswell so can render into the usertab
def get_clothes_by_user(username):
    clothes = Clothing.query.filter_by(username=username).all()
    return render_template("usertab.html", clothes=clothes, username=username)
