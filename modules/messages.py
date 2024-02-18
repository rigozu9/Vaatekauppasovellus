# module for message functions
from models import Message, Chat, Clothing, User
from db import db
from flask import request, redirect, render_template, session
from datetime import datetime

def get_messages(sender_username, receiver_username, garment_id):
    garment = Clothing.query.get(garment_id)
    
    # Retrieve messages where sender can be either buyer or seller, and receiver can be either buyer or seller
    messages = Message.query.filter(
        (Message.sender_username == sender_username) & (Message.receiver_username == receiver_username) |
        (Message.sender_username == receiver_username) & (Message.receiver_username == sender_username),
        Message.item_id == garment_id
    ).all()
    if 'username' in session:
        user = User.query.filter_by(username=session['username']).first()
        return render_template('item_messages.html', messages=messages, sender_username=sender_username, receiver_username=receiver_username, garment=garment, user=user)
    else:
        return render_template('item_messages.html', messages=messages, sender_username=sender_username, receiver_username=receiver_username, garment=garment)

# Sending a message
def send_message():
    sender_username = request.form.get('sender_username')
    receiver_username = request.form.get('receiver_username')
    item_id = request.form.get('item_id')
    message_body = request.form.get('message_body')

    timestamp = datetime.now()

    # Check if a chat exists between sender and receiver for the item
    existing_chat = Chat.query.filter_by(buyer_username=sender_username,
                                          seller_username=receiver_username,
                                          item_id=item_id).first()

    if not existing_chat:
        # Create a new chat if one doesn't exist
        new_chat = Chat(buyer_username=sender_username,
                        seller_username=receiver_username,
                        item_id=item_id,
                        start_timestamp=timestamp)
        db.session.add(new_chat)
        db.session.commit()

        chat_id = new_chat.id
    else:
        # Use the existing chat_id
        chat_id = existing_chat.id

    # Create a new message object
    new_message = Message(chat_id=chat_id,
                          sender_username=sender_username,
                          receiver_username=receiver_username,
                          item_id=item_id,
                          message_body=message_body,
                          timestamp=timestamp)

    # Add the new message to the database session and commit changes
    db.session.add(new_message)
    db.session.commit()

    # Redirect to the chat
    return redirect(f"/send_message/{sender_username}/{receiver_username}/{item_id}")
