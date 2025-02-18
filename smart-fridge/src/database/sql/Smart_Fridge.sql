CREATE TABLE IF NOT EXISTS Users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    pincode DOUBLE NOT NULL,
    active BOOLEAN NOT NULL DEFAULT False,
);

CREATE TABLE IF NOT EXISTS Fridges (
    fridge_guid TEXT PRIMARY KEY,
    model JSON NOT NULL,
);

CREATE TABLE IF NOT EXISTS Connections (
    connection_id INTEGER PRIMARY KEY AUTOINCREMENT,
    fridge_guid TEXT NOT NULL,
    user_id INTEGER NOT NULL,

    FOREIGN KEY (fridge_guid) REFERENCES Fridges(fridge_guid),
    FOREIGN KEY (user_id) REFERENCES Users(user_id)
);

CREATE TABLE IF NOT EXISTS Items (
    item_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    quantity UNSIGNED REAL CHECK(quantity > 0),
    expiration_date DATE,

    fridge_guid TEXT NOT NULL,
    list_id INTEGER DEFAULT NULL,
    user_id INTEGER,

    FOREIGN KEY (fridge_guid) REFERENCES Fridges(fridge_guid),
    FOREIGN KEY (list_id) REFERENCES ShoppingLists(list_id)
);

CREATE TABLE IF NOT EXISTS Sensors (
    sensor_id INTEGER PRIMARY KEY AUTOINCREMENT,
    sensor_type TEXT NOT NULL,
    value REAL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fridge_guid TEXT NOT NULL,

    FOREIGN KEY (fridge_guid) REFERENCES Fridges(fridge_guid)
);

CREATE TABLE IF NOT EXISTS ShoppingLists (
    list_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    created_date DATE,

    fridge_guid TEXT NOT NULL,
    user_id INTEGER NOT NULL,

    FOREIGN KEY (fridge_guid) REFERENCES Items(fridge_guid),
    FOREIGN KEY (user_id) REFERENCES Users(user_id)
);
