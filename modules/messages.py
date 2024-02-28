# module for message functions
from db import db
from flask import request, redirect, render_template, session
from datetime import datetime
from sqlalchemy import text

def get_messages(sender_username, receiver_username, garment_id):
    garment_query = text("SELECT * FROM clothes WHERE id = :garment_id")
    garment = db.session.execute(garment_query, {"garment_id": garment_id}).fetchone()
    
    # Retrieve messages where sender can be either buyer or seller, and receiver can be either buyer or seller
    query = text("""
        SELECT * FROM messages
        WHERE ((sender_username = :sender_username AND receiver_username = :receiver_username) 
        OR (sender_username = :receiver_username AND receiver_username = :sender_username))
        AND item_id = :garment_id
        """)
    messages = db.session.execute(query, {"sender_username": sender_username, "receiver_username": receiver_username, "garment_id": garment_id}).fetchall()

    if 'username' in session:
        username = session['username']
        user_query = text("SELECT * FROM users WHERE username = :username")
        user = db.session.execute(user_query, {"username": username}).first()
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

    existing_chat_query = text("""
        SELECT * FROM chats
        WHERE (buyer_username = :sender_username AND seller_username = :receiver_username
            OR buyer_username = :receiver_username AND seller_username = :sender_username)
        AND item_id = :item_id
    """)
    existing_chat = db.session.execute(existing_chat_query, {
        "sender_username": sender_username, 
        "receiver_username": receiver_username, 
        "item_id": item_id
    }).first()

    if not existing_chat:
        # Create a new chat if one doesn't exist
        new_chat_query = text("""
            INSERT INTO chats (buyer_username, seller_username, item_id, start_timestamp)
            VALUES (:sender_username, :receiver_username, :item_id, :start_timestamp)
            RETURNING id
            """)
        result = db.session.execute(new_chat_query, {
            "sender_username": sender_username, 
            "receiver_username": receiver_username, 
            "item_id": item_id, 
            "start_timestamp": timestamp
        })
        db.session.commit()

        chat_id = result.fetchone()[0]
    else:
        # Use the existing chat_id
        chat_id = existing_chat.id

    # Create a new message object
    new_message_query = text("""
    INSERT INTO messages (chat_id, sender_username, receiver_username, item_id, message_body, timestamp)
    VALUES (:chat_id, :sender_username, :receiver_username, :item_id, :message_body, :timestamp)
    """)

    db.session.execute(new_message_query, {"chat_id": chat_id, "sender_username": sender_username, "receiver_username": receiver_username, "item_id": item_id, "message_body": message_body, "timestamp": timestamp})
    db.session.commit()

    # Redirect to the chat
    return redirect(f"/send_message/{sender_username}/{receiver_username}/{item_id}")
