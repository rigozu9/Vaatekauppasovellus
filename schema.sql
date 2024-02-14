-- Create the 'users' table
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL
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

-- Create the 'clothes' table with foreign key references
CREATE TABLE clothes (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description VARCHAR(255) NOT NULL,
    brand VARCHAR(255) NOT NULL,
    category VARCHAR(255) NOT NULL,
    size VARCHAR(255) NOT NULL,
    price FLOAT NOT NULL,
    username VARCHAR(255) REFERENCES users(username)
);

-- Create the 'images' table with foreign key references
CREATE TABLE images (
    id SERIAL PRIMARY KEY,
    clothing_id INTEGER REFERENCES clothes(id) ON DELETE CASCADE,
    data BYTEA NOT NULL
);

-- Create the 'messages' table
CREATE TABLE messages (
    id SERIAL PRIMARY KEY,
    sender_username INTEGER REFERENCES users(username),
    receiver_username INTEGER REFERENCES users(username),
    item_id INTEGER REFERENCES clothes(id),
    message_body TEXT NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
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

Example data for clothes. Need users to insert
INSERT INTO clothes (name, description, brand, category, size, price, username)
VALUES 
    ('Nike shirt', 'Cotton t-shirt', 'Nike', 'tops', 'M', 50, 'rigozu9'),
    ('Blue jeans', 'Blue denim jeans', 'Levi''s', 'bottoms', 'XL', 100, 'rigozu9'),
    ('Adidas sneakers', 'White canvas sneakers', 'Adidas', 'footwear', 'Other', 79, '123');
