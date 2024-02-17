#module for user related functions
from flask import render_template
from sqlalchemy import desc, or_
from models import Clothing, Chat, Message

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
    return render_template("usertab.html", last_messages=last_messages, clothes=clothes, username=username, chats=chats)