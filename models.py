#Clothes class to set up model
from db import db

#Clothes model with id, name, description, brand, category, size, price, 
#the user who added it and the uploaded image_path. 
class Clothing(db.Model):
    __tablename__ = 'clothes'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    brand = db.Column(db.String(255), nullable=False)
    category = db.Column(db.String(255), nullable=False)
    size = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Float, nullable=False)
    username = db.Column(db.String(255), db.ForeignKey('users.id'))
    image_path = db.Column(db.String(255))

    def __repr__(self):
        return f'<Clothes {self.name}>'

#User model for registering an account. Has unique id, unique, username and password.
class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)

    def __repr__(self):
        return f'<User {self.username}>'

#Category model
class Category(db.Model):
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return f'<Category {self.name}>'
    
#Brand model
class Brand(db.Model):
    __tablename__ = 'brands'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return f'<Brand {self.name}>'
    
#Size model
class Size(db.Model):
    __tablename__ = 'sizes'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return f'<Brand {self.name}>'