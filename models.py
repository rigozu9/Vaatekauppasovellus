#Clothes class to set up model
from db import db

#Clothes model with id and name of the garment. Returns name of the garment.
class Clothes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return f'<Clothes {self.name}>'

#User model for registering an account. Has unique id, unique, username and password
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)