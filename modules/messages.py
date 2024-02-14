# module for message functions
from models import Message
from db import db
from flask import request, redirect
from datetime import datetime

#sending a message
def send_message():
    sender_username = request.form.get('sender_username')
    receiver_username = request.form.get('receiver_username')
    item_id = request.form.get('item_id')
    message_body = request.form.get('message_body')

    print(f"Sending message for item_id: {item_id}")

    timestamp = datetime.now()

    # Create a new message object
    new_message = Message(
        sender_username=sender_username,
        receiver_username=receiver_username,
        item_id=item_id,
        message_body=message_body,
        timestamp=timestamp
    )

    # Add the new message to the database session and commit changes
    db.session.add(new_message)
    db.session.commit()

    # Redirect the user to a suitable route
    return redirect(f"/garment/{item_id}")
