#module for user related functions
from flask import render_template, session, flash, redirect, request
from db import db
from sqlalchemy import text

# Method to get info from the username
def get_info_by_user(username):
    # Fetch clothes using SQL command
    clothes_query = text("""
        SELECT c.*, i.data AS image_data
        FROM clothes c
        LEFT JOIN (
            SELECT clothing_id, data,
                ROW_NUMBER() OVER (PARTITION BY clothing_id ORDER BY main_image DESC, id) AS rn  
            FROM images
        ) i ON c.id = i.clothing_id AND i.rn = 1
        WHERE c.username = :username
    """)
    clothes = db.session.execute(clothes_query, {"username": username}).fetchall()
    
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
    clothing_query = text("""
        SELECT *
        FROM clothes
        WHERE id = :garment_id
    """)

    old_garment = db.session.execute(clothing_query, {"garment_id": garment_id}).fetchone()

    buyer = session.get('username')
    seller = old_garment.username

    seller_query = text("""
        SELECT * FROM users WHERE username = :seller
    """)
    seller_user = db.session.execute(seller_query, {"seller": seller}).fetchone()

    buyer_query = text("""
        SELECT * FROM users WHERE username = :buyer
    """)
    buyer_user = db.session.execute(buyer_query, {"buyer": buyer}).fetchone()

    # Check if the buyer has enough balance to purchase the item
    if buyer_user.balance < old_garment.price:
        flash("Insufficient balance to purchase this item", "error")
        return redirect(f"/garment/{garment_id}")

    update_buyer_balance_query = text("""
        UPDATE users
        SET balance = balance - :price
        WHERE username = :buyer
    """)
    db.session.execute(update_buyer_balance_query, {"price": old_garment.price, "buyer": buyer})

    update_seller_balance_query = text("""
        UPDATE users
        SET balance = balance + :price
        WHERE username = :seller
    """)
    db.session.execute(update_seller_balance_query, {"price": old_garment.price, "seller": seller})

    update_status_query = text("""
        UPDATE clothes
        SET status = 'sold'
        WHERE id = :garment_id
    """)

    db.session.execute(update_status_query, {"garment_id": garment_id})

    # Create a new clothing entry for the buyer with status "bought"
    new_clothing_query = text("""
        INSERT INTO clothes (name, description, brand, category, size, price, username, status)
        VALUES (:name, :description, :brand, :category, :size, :price, :username, 'bought')
        RETURNING id
    """)

    new_clothing_params = {
        "name": old_garment.name,
        "description": old_garment.description,
        "brand": old_garment.brand,
        "category": old_garment.category,
        "size": old_garment.size,
        "price": old_garment.price,
        "username": buyer
    }

    new_clothing_result = db.session.execute(new_clothing_query, new_clothing_params)
    new_clothing_id = new_clothing_result.fetchone()[0]

    new_clothing_query = text("""
        SELECT *
        FROM clothes
        WHERE id = :new_clothing_id
    """)

    clothing_result = db.session.execute(new_clothing_query, {"new_clothing_id": new_clothing_id}).fetchone()

    # Fetch images associated with the clothing item
    images_query = text("""
        SELECT data
        FROM images
        WHERE clothing_id = :garment_id
    """)

    images_result = db.session.execute(images_query, {"garment_id": garment_id}).fetchall()

    # Copy images from the original garment to the newly bought garment
    for image in images_result:
        new_image_query = text("""
            INSERT INTO images (clothing_id, data)
            VALUES (:clothing_id, :data)
        """)
        new_image_params = {
            "clothing_id": new_clothing_id,
            "data": image.data
        }
        db.session.execute(new_image_query, new_image_params)

    # Create a new transaction
    new_transaction_query = text("""
        INSERT INTO transactions (seller_username, buyer_username, price, item_id)
        VALUES (:seller_username, :buyer_username, :price, :item_id)
    """)
    new_transaction_params = {
        "seller_username": seller,
        "buyer_username": buyer,
        "price": old_garment.price,
        "item_id": garment_id
    }
    db.session.execute(new_transaction_query, new_transaction_params)

    # Fetch images associated with the clothing item
    images_query = text("""
        SELECT data
        FROM images
        WHERE clothing_id = :garment_id
    """)

    images_result = db.session.execute(images_query, {"garment_id": garment_id}).fetchall()

    image_data_list = [row[0] for row in images_result]

    db.session.commit()

    # Render the bought page template
    return render_template("bought_page.html", garment=clothing_result, seller=seller, images=image_data_list)

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
