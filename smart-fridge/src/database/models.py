from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Users(db.Model):
    __tablename__ = 'Users'
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String, nullable=False)
    pincode = db.Column(db.String, nullable=False)
    preferences = db.Column(db.String)

class Fridges(db.Model):
    __tablename__ = 'Fridges'
    fridge_guid = db.Column(db.String, primary_key=True)
    model = db.Column(db.JSON)

class Connections(db.Model):
    __tablename__ = 'Connections'
    connection_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    fridge_guid = db.Column(db.String, db.ForeignKey('Fridges.fridge_guid'))
    user_id = db.Column(db.Integer, db.ForeignKey('Users.user_id'))

class Items(db.Model):
    __tablename__ = 'Items'
    item_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    quantity = db.Column(db.Float)
    expiration_date = db.Column(db.Date)
    fridge_guid = db.Column(db.Integer, db.ForeignKey('Fridges.fridge_guid'))
    #user_id = db.Column(db.Integer, db.ForeignKey('Users.user_id'))

class Sensors(db.Model):
    __tablename__ = 'Sensors'
    sensor_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    sensor_type = db.Column(db.String, nullable=False)
    value = db.Column(db.Float)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    fridge_guid = db.Column(db.Integer, db.ForeignKey('Fridges.fridge_guid'))

class ShoppingLists(db.Model):
    __tablename__ = 'ShoppingLists'
    list_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    created_date = db.Column(db.Date)
    user_id = db.Column(db.Integer, db.ForeignKey('Users.user_id'))

#class ListItems(db.Model):
#    __tablename__ = 'ListItems'
#    list_item_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#    list_id = db.Column(db.Integer, db.ForeignKey('ShoppingLists.list_id'))
#    item_id = db.Column(db.Integer, db.ForeignKey('Items.item_id'))
#    quantity = db.Column(db.Float)
