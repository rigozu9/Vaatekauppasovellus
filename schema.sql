-- Create the 'users' table
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    role VARCHAR(255),
    balance FLOAT
);

-- Create the 'categories' table
CREATE TABLE categories (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL
);

-- Create the 'brands' table
CREATE TABLE brands (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL
);

-- Create the 'sizes' table
CREATE TABLE sizes (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL
);

-- Create the 'clothes' table with foreign key references added status for the availablity
CREATE TABLE clothes (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description VARCHAR(255) NOT NULL,
    brand VARCHAR(255) NOT NULL,
    category VARCHAR(255) NOT NULL,
    size VARCHAR(255) NOT NULL,
    price FLOAT NOT NULL,
    username VARCHAR(255) REFERENCES users(username),
    status VARCHAR(50) DEFAULT 'available' 
);

-- Create the 'images' table with foreign key references
CREATE TABLE images (
    id SERIAL PRIMARY KEY,
    clothing_id INTEGER REFERENCES clothes(id) ON DELETE CASCADE,
    data BYTEA NOT NULL
);

-- Create the chats table
CREATE TABLE chats (
    id SERIAL PRIMARY KEY,
    buyer_username VARCHAR(255) REFERENCES users(username) NOT NULL,
    seller_username VARCHAR(255) REFERENCES users(username) NOT NULL,
    item_id INTEGER REFERENCES clothes(id) NOT NULL,
    start_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create the messages table
CREATE TABLE messages (
    id SERIAL PRIMARY KEY,
    chat_id INTEGER REFERENCES chats(id) NOT NULL,
    sender_username VARCHAR(255) REFERENCES users(username) NOT NULL,
    receiver_username VARCHAR(255) REFERENCES users(username) NOT NULL,
    item_id INTEGER REFERENCES clothes(id) NOT NULL,
    message_body TEXT NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create the transactions table
CREATE TABLE transactions (
    id SERIAL PRIMARY KEY,
    seller_username VARCHAR(255) NOT NULL,
    buyer_username VARCHAR(255) NOT NULL,
    price FLOAT NOT NULL,
    item_id INTEGER NOT NULL,
    FOREIGN KEY (seller_username) REFERENCES users(username),
    FOREIGN KEY (buyer_username) REFERENCES users(username),
    FOREIGN KEY (item_id) REFERENCES clothes(id)
);


INSERT INTO categories (name) VALUES ('tops');
INSERT INTO categories (name) VALUES ('bottoms');
INSERT INTO categories (name) VALUES ('footwear');
INSERT INTO categories (name) VALUES ('other');


INSERT INTO brands (name) VALUES ('BAPE');
INSERT INTO brands (name) VALUES ('NUMBER (N)INE');
INSERT INTO brands (name) VALUES ('junya watanabe');
INSERT INTO brands (name) VALUES ('All brands');

INSERT INTO sizes (name) VALUES ('S');
INSERT INTO sizes (name) VALUES ('M');
INSERT INTO sizes (name) VALUES ('L');
INSERT INTO sizes (name) VALUES ('XL');
INSERT INTO sizes (name) VALUES ('Other');

ALTER TABLE images ADD COLUMN main_image BOOLEAN DEFAULT FALSE;
