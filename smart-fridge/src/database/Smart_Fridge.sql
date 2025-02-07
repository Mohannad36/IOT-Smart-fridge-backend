CREATE TABLE Users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    preferences TEXT
);

CREATE TABLE Fridges (
    fridge_id INTEGER PRIMARY KEY AUTOINCREMENT,
    location TEXT,
    model TEXT,
    user_id INTEGER,
    FOREIGN KEY (user_id) REFERENCES Users(user_id)
);

CREATE TABLE Items (
    item_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    quantity REAL,
    expiration_date DATE,
    fridge_id INTEGER,
    user_id INTEGER,
    weight_sensor_id INTEGER,
    FOREIGN KEY (user_id) REFERENCES Users(user_id),
    FOREIGN KEY (fridge_id) REFERENCES Fridges(fridge_id),
    FOREIGN KEY (weight_sensor_id) REFERENCES Sensors(sensor_id)
);

CREATE TABLE Sensors (
    sensor_id INTEGER PRIMARY KEY AUTOINCREMENT,
    sensor_type TEXT NOT NULL,
    value REAL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fridge_id INTEGER,
    FOREIGN KEY (fridge_id) REFERENCES Fridges(fridge_id)
);

CREATE TABLE ShoppingLists (
    list_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    created_date DATE,
    user_id INTEGER,
    FOREIGN KEY (user_id) REFERENCES Users(user_id)
);

CREATE TABLE ListItems (
    list_item_id INTEGER PRIMARY KEY AUTOINCREMENT,
    list_id INTEGER,
    item_id INTEGER,
    quantity REAL,
    FOREIGN KEY (list_id) REFERENCES ShoppingLists(list_id),
    FOREIGN KEY (item_id) REFERENCES Items(item_id)
);
