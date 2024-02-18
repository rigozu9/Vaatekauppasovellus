#module for user related functions
from flask import render_template, session, flash, redirect, request
from sqlalchemy import desc, or_
from models import Clothing, Chat, Message, User, Transaction, Image
from db import db

# Method to get info from the username
def get_info_by_user(username):
    clothes = Clothing.query.filter_by(username=username).all()
    chats = Chat.query.filter(
        or_(
            Chat.seller_username == username,
            Chat.buyer_username == username
        )
    ).all()
    last_messages = {}
    for chat in chats:
        last_message = Message.query.filter_by(chat_id=chat.id).order_by(desc(Message.timestamp)).first()
        last_messages[chat.id] = last_message
    
    user = User.query.filter_by(username=session['username']).first()
    return render_template("usertab.html", last_messages=last_messages, clothes=clothes, username=username, chats=chats, user=user)

#Clothing buying method
def buy_clothing(garment_id):
    garment = Clothing.query.get(garment_id)
    
    buyer = session.get('username')
    seller = garment.username

    seller_user = User.query.filter_by(username=seller).first()
    buyer_user = User.query.filter_by(username=buyer).first()

    # Check if the buyer has enough balance to purchase the item
    if buyer_user.balance < garment.price:
        flash("Insufficient balance to purchase this item", "error")
        return redirect(f"/garment/{garment_id}")

    buyer_user.balance -= garment.price

    seller_user.balance += garment.price

    garment.status = "sold"

    # Create a new clothing entry for the buyer with status "bought"
    new_clothing_for_buyer = Clothing(
        name=garment.name,
        description=garment.description,
        brand=garment.brand,
        category=garment.category,
        size=garment.size,
        price=garment.price,
        username=buyer,
        status="bought"
    )
    db.session.add(new_clothing_for_buyer)
    db.session.commit()

    for image in garment.images:
        new_image = Image(
            clothing_id=new_clothing_for_buyer.id,
            data=image.data
        )
        db.session.add(new_image)

    db.session.commit()

    # Create a new transaction
    new_transaction = Transaction(
        seller_username=seller,
        buyer_username=buyer,
        price=garment.price,
        item_id=garment_id
    )

    # Add the transaction to the database session
    db.session.add(new_transaction)
    db.session.commit()

    # Render the bought page template
    return render_template("bought_page.html", garment=new_clothing_for_buyer, seller=seller)

def get_chats(seller_username, garment_id):
    garment = Clothing.query.get(garment_id)
    # Fetch chats where the user is the seller and the item_id matches
    chats = Chat.query.filter(
        Chat.seller_username == seller_username,
        Chat.item_id == garment_id
    ).all()

    # Fetch the last message for each chat
    last_messages = {}
    for chat in chats:
        last_message = Message.query.filter_by(chat_id=chat.id).order_by(desc(Message.timestamp)).first()
        last_messages[chat.id] = last_message
    user = User.query.filter_by(username=session['username']).first()
    return render_template('chats.html', chats=chats, last_messages=last_messages, seller_username=seller_username, garment=garment, user=user)


# Balance adding method
def add_balance():
    user = User.query.filter_by(username=session['username']).first()
    balance_to_add = float(request.form.get('balance', 0))

    user.balance += balance_to_add
    db.session.commit()

    return redirect(f"/users/{user.username}")