#database using psql and python env
from app import app
from flask_sqlalchemy import SQLAlchemy
from os import getenv

#For deployment
#app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL").replace("://", "ql://", 1)

#For local
app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")

app.secret_key = getenv("SECRET_KEY")

db = SQLAlchemy(app)
