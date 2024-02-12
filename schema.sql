CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL
);

CREATE TABLE categories (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL
);

CREATE TABLE brands (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL
);

CREATE TABLE sizes (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL
);

CREATE TABLE clothes (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description VARCHAR(255) NOT NULL,
    brand VARCHAR(255) NOT NULL,
    category VARCHAR(255) NOT NULL,
    size VARCHAR(255) NOT NULL,
    price FLOAT NOT NULL,
    username VARCHAR(50) REFERENCES users(username),
    image_path VARCHAR(255)
);

INSERT INTO categories (name) VALUES ('Tops');
INSERT INTO categories (name) VALUES ('Bottoms');
INSERT INTO categories (name) VALUES ('Footwear');
INSERT INTO categories (name) VALUES ('Other');


INSERT INTO brands (name) VALUES ('BAPE');
INSERT INTO brands (name) VALUES ('NUMBER (N)INE');
INSERT INTO brands (name) VALUES ('junya watanabe');
INSERT INTO brands (name) VALUES ('All brands');

INSERT INTO sizes (name) VALUES ('S');
INSERT INTO sizes (name) VALUES ('M');
INSERT INTO sizes (name) VALUES ('L');
INSERT INTO sizes (name) VALUES ('XL');
INSERT INTO sizes (name) VALUES ('Other');