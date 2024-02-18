#module for user related functions
from flask import render_template, session
from sqlalchemy import desc, or_
from models import Clothing, Chat, Message, User

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

def buy_clothing(garment_id):
    return render_template("bought_page.html", garment_id=garment_id) 

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

