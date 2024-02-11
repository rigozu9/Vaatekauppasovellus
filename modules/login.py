#login module for the functions register, login and logout
from flask import redirect, render_template, request, session
from werkzeug.security import check_password_hash, generate_password_hash
from db import db
from models import User

#registering a new account using User model
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        
        hash_value = generate_password_hash(password)

        new_user = User(username=username, password=hash_value)

        db.session.add(new_user)
        db.session.commit()

        session["username"] = username
        return redirect("/")
    return render_template("register.html")

#check if the credentials are correct if they are sign in
def login():
    render_template("login.html", error=None)
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user = User.query.filter_by(username=username).first()

        if not user or not check_password_hash(user.password, password):
            return render_template("login.html", error="Invalid username or password")

        session["username"] = username
        return redirect("/")
    return render_template("login.html")

#log out
def logout():
    session.pop("username", None)
    return redirect("/")
