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

    # Define the one-to-many relationship with Image
    images = db.relationship('Image', backref='clothing', lazy=True)

    def __repr__(self):
        return f'<Clothes {self.name}>'
    
#Table for images that are connected to a listing by clothes.id
class Image(db.Model):
    __tablename__ = 'images'

    id = db.Column(db.Integer, primary_key=True)
    clothing_id = db.Column(db.Integer, db.ForeignKey('clothes.id'), nullable=False)
    data = db.Column(db.LargeBinary, nullable=False)

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

#Added a chat model to store chats
class Chat(db.Model):
    __tablename__ = 'chats'

    id = db.Column(db.Integer, primary_key=True)
    buyer_username = db.Column(db.String(255), db.ForeignKey('users.username'), nullable=False)
    seller_username = db.Column(db.String(255), db.ForeignKey('users.username'), nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey('clothes.id'), nullable=False)
    start_timestamp = db.Column(db.TIMESTAMP, server_default=db.func.now())

    buyer = db.relationship("User", foreign_keys=[buyer_username])
    seller = db.relationship("User", foreign_keys=[seller_username])
    item = db.relationship("Clothing")

    messages = db.relationship("Message", backref="associated_chat", lazy="dynamic")

    def __repr__(self):
        return f'<Chat {self.id}>'    

# Message model
class Message(db.Model):
    __tablename__ = 'messages'

    id = db.Column(db.Integer, primary_key=True)
    chat_id = db.Column(db.Integer, db.ForeignKey('chats.id'), nullable=False)
    sender_username = db.Column(db.String(255), db.ForeignKey('users.username'), nullable=False)
    receiver_username = db.Column(db.String(255), db.ForeignKey('users.username'), nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey('clothes.id'), nullable=False)
    message_body = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.TIMESTAMP, server_default=db.func.now())

    sender = db.relationship("User", foreign_keys=[sender_username])
    receiver = db.relationship("User", foreign_keys=[receiver_username])
    item = db.relationship("Clothing")
    chat = db.relationship("Chat")

    def __repr__(self):
        return f'<Message {self.id}>'

    