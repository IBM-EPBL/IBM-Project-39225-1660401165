DROP TABLE IF EXISTS users;

CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    password TEXT NOT NULL,
    name TEXT NOT NULL,
    email TEXT NOT NULL
);

INSERT INTO users (username, password, name, email) VALUES (
    "kiruba-r11",
    "dbpassword",
    "kiruba",
    "19cs121@psgitech.ac.in"
);