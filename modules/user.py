#module for user related functions
from flask import render_template, session, flash, redirect, request
from db import db
from sqlalchemy import text
from models import User, Transaction, Clothing, Image

# Method to get info from the username
def get_info_by_user(username):
    # Fetch clothes using SQL command
    clothes = Clothing.query.filter_by(username=username).all()
    
    # Fetch chats using SQL command
    chats_query = text("""
    SELECT * FROM chats
    WHERE seller_username = :username OR buyer_username = :username
    """)
    chats = db.session.execute(chats_query, {"username": username}).fetchall()

    last_messages = {}
    for chat in chats:
        last_message_query = text("""
        SELECT * FROM messages
        WHERE chat_id = :chat_id
        ORDER BY timestamp DESC
        LIMIT 1
        """)
        last_message = db.session.execute(last_message_query, {"chat_id": chat.id}).fetchone()
        last_messages[chat.id] = last_message
    
    user_query = text("SELECT * FROM users WHERE username = :username")
    user = db.session.execute(user_query, {"username": session['username']}).first()
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
    # Fetch garment details using SQL command
    garment_query = text("SELECT * FROM clothes WHERE id = :garment_id")
    garment = db.session.execute(garment_query, {"garment_id": garment_id}).fetchone()
    
    # Fetch chats where the user is the seller and the item_id matches
    chats_query = text("""
    SELECT * FROM chats
    WHERE seller_username = :seller AND item_id = :garment_id
    """)
    chats = db.session.execute(chats_query, {"seller": seller_username, "garment_id": garment_id}).fetchall()

    # Fetch the last message for each chat
    last_messages = {}
    for chat in chats:
        last_message_query = text("""
        SELECT * FROM messages
        WHERE chat_id = :chat_id
        ORDER BY timestamp DESC
        LIMIT 1
        """)
        last_message = db.session.execute(last_message_query, {"chat_id": chat.id}).fetchone()
        last_messages[chat.id] = last_message

    user_query = text("SELECT * FROM users WHERE username = :username")
    user = db.session.execute(user_query, {"username": session['username']}).first()
    return render_template('chats.html', chats=chats, last_messages=last_messages, seller_username=seller_username, garment=garment, user=user)

# Balance adding method
def add_balance():
    # Retrieve the user from the database using a raw SQL query
    sql_query = text("SELECT * FROM users WHERE username = :username")
    result = db.session.execute(sql_query, {"username": session['username']})
    user = result.fetchone()

    if user:
        # Get the balance to add from the form
        balance_to_add = float(request.form.get('balance', 0))

        # Update the user's balance using a raw SQL UPDATE query
        update_query = text("UPDATE users SET balance = balance + :balance_to_add WHERE username = :username")
        db.session.execute(update_query, {"balance_to_add": balance_to_add, "username": session['username']})
        db.session.commit()

    return redirect(f"/users/{session['username']}")
