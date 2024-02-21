from flask import redirect, render_template, request, session
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy.exc import IntegrityError
from db import db
from sqlalchemy import text

# Registering a new account using raw SQL commands
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        
        hash_value = generate_password_hash(password)

        try:
            # Insert new user into the database
            new_user_query = text("""
                INSERT INTO users (username, password, balance)
                VALUES (:username, :password, :balance)
            """)
            db.session.execute(new_user_query, {"username": username, "password": hash_value, "balance": 0.0})
            db.session.commit()

            session["username"] = username
            return redirect("/")
        except IntegrityError:
            db.session.rollback()
            error_message = "Username already exists. Please choose a different one."
            return render_template("register.html", error_message=error_message)
    return render_template("register.html")

# Check if the credentials are correct, if they are, sign in
def login():
    render_template("login.html", error=None)
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        # Retrieve user from the database
        user_query = text("SELECT * FROM users WHERE username = :username")
        user = db.session.execute(user_query, {"username": username}).fetchone()

        if not user or not check_password_hash(user.password, password):
            return render_template("login.html", error="Invalid username or password")

        session["username"] = username
        return redirect("/")
    return render_template("login.html")

# Logout
def logout():
    session.pop("username", None)
    return redirect("/")
