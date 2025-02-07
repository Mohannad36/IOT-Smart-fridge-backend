from datetime import datetime
from . import db

class User(db.Model):
    __tablename__ = 'Users'
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String, nullable=False)
    preferences = db.Column(db.String)

class Fridge(db.Model):
    __tablename__ = 'Fridges'
    fridge_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    location = db.Column(db.String)
    model = db.Column(db.String)
    user_id = db.Column(db.Integer, db.ForeignKey('Users.user_id'))

class Item(db.Model):
    __tablename__ = 'Items'
    item_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    quantity = db.Column(db.Float)
    expiration_date = db.Column(db.Date)
    fridge_id = db.Column(db.Integer, db.ForeignKey('Fridges.fridge_id'))
    user_id = db.Column(db.Integer, db.ForeignKey('Users.user_id'))

class Sensor(db.Model):
    __tablename__ = 'Sensors'
    sensor_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    sensor_type = db.Column(db.String, nullable=False)
    value = db.Column(db.Float)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    fridge_id = db.Column(db.Integer, db.ForeignKey('Fridges.fridge_id'))

class ShoppingList(db.Model):
    __tablename__ = 'ShoppingLists'
    list_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    created_date = db.Column(db.Date)
    user_id = db.Column(db.Integer, db.ForeignKey('Users.user_id'))

class ListItem(db.Model):
    __tablename__ = 'ListItems'
    list_item_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    list_id = db.Column(db.Integer, db.ForeignKey('ShoppingLists.list_id'))
    item_id = db.Column(db.Integer, db.ForeignKey('Items.item_id'))
    quantity = db.Column(db.Float)
