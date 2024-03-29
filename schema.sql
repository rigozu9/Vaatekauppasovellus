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

CREATE TABLE subcategories (
    id SERIAL PRIMARY KEY,
    category_id INTEGER REFERENCES categories(id) ON DELETE CASCADE,
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

CREATE TABLE category_sizes (
    id SERIAL PRIMARY KEY,
    category_id INTEGER NOT NULL REFERENCES categories(id),
    size_id INTEGER NOT NULL REFERENCES sizes(id),
    UNIQUE(category_id, size_id)
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

INSERT INTO sizes (name) VALUES 
('US26/EU42'), 
('US27'), 
('US28/EU44'), 
('US29'), 
('US30/EU46'), 
('US31'),
('US32/EU48'), 
('US33'), 
('US34/EU50'), 
('US35'), 
('US36/EU52'), 
('US37'), 
('US38/EU54'), 
('US39'), 
('US40/EU56');
INSERT INTO sizes (name) VALUES
('EU34'), ('EU35'), ('EU36'), ('EU37'), ('EU38'), ('EU39'), 
('EU40'), ('EU41'), ('EU42'), ('EU43'), ('EU44'), 
('EU45'), ('EU46'), ('EU47'), ('EU48'), ('EU49');

INSERT INTO category_sizes (category_id, size_id) VALUES
(1, (SELECT id FROM sizes WHERE name = 'XXS')),
(1, (SELECT id FROM sizes WHERE name = 'XS')),
(1, (SELECT id FROM sizes WHERE name = 'S')),
(1, (SELECT id FROM sizes WHERE name = 'M')),
(1, (SELECT id FROM sizes WHERE name = 'L')),
(1, (SELECT id FROM sizes WHERE name = 'XL')),
(1, (SELECT id FROM sizes WHERE name = 'XXL'));


ALTER TABLE images ADD COLUMN main_image BOOLEAN DEFAULT FALSE;
