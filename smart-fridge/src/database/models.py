from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import CheckConstraint
from sqlalchemy.dialects.mysql import INTEGER
from datetime import datetime

db = SQLAlchemy()

class Users(db.Model):
    __tablename__ = 'Users'
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String, nullable=False)
    pincode = db.Column(db.Double, nullable=False)
    active = db.Column(db.Boolean, nullable=False, default=False)

class Fridges(db.Model):
    __tablename__ = 'Fridges'
    fridge_guid = db.Column(db.String, primary_key=True)
    model = db.Column(db.JSON, nullable=False)

class Connections(db.Model):
    __tablename__ = 'Connections'
    connection_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    fridge_guid = db.Column(db.String, db.ForeignKey('Fridges.fridge_guid'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('Users.user_id'), nullable=False)

class Items(db.Model):
    __tablename__ = 'Items'
    item_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    quantity = db.Column(INTEGER(unsigned=True))
    expiration_date = db.Column(db.Date)

    fridge_guid = db.Column(db.String, db.ForeignKey('Fridges.fridge_guid'), nullable=False)
    list_id = db.Column(db.Integer, db.ForeignKey('ShoppingLists.list_id'), nullable=False)
    user_id = db.Column(db.Integer)

    CheckConstraint("quantity > 0", name="Check for minimum quantity")

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

    fridge_guid = db.Column(db.String, db.ForeignKey('Items.fridge_guid'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('Users.user_id'), nullable=False)
