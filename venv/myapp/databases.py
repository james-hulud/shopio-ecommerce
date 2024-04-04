from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime
from time import strftime

db = SQLAlchemy()

class Products(db.Model):
    __tablename__ = "products"
    id = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.String(100))
    price = db.Column(db.String(100))
    description = db.Column(db.Text)
    image = db.Column(db.String(100))
    env_impact = db.Column(db.Text)

class User(db.Model, UserMixin):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True, unique=True)
    email = db.Column(db.String(30), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)
    username = db.Column(db.String(20), nullable=False, unique=True)
    creation_date = db.Column(db.String(), default=datetime.now(datetime.now().astimezone().tzinfo).isoformat())
    
    # back_populates 'user' specifies the attribute in the related table, here it is 'user_ad' in Address
    address = db.relationship('Address', back_populates='user_ad', uselist=False)
    
    payment_details = db.relationship('PaymentDetails', back_populates='user_pd', uselist=False)
    
class Address(db.Model):
    __tablename__ = "address"
    id = db.Column(db.Integer, primary_key=True, unique=True)
    full_name = db.Column(db.String(100), nullable=False)
    phone_number = db.Column(db.String(20), nullable=False)
    postcode = db.Column(db.String(20), nullable=False)
    address_line_one = db.Column(db.String(100), nullable=False)
    address_line_two = db.Column(db.String(100), nullable=False)
    town_city = db.Column(db.String(100), nullable=False)
    county = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user_ad = db.relationship('User', back_populates='address')
    
class PaymentDetails(db.Model):
    __tablename__ = 'payment_details'
    id = db.Column(db.Integer, primary_key=True, unique=True)
    name_on_card = db.Column(db.String(), nullable=False)
    card_number = db.Column(db.String(16), nullable=False)
    expiry_date = db.Column(db.String(8), nullable=False)
    security_number = db.Column(db.String(3), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user_pd = db.relationship('User', back_populates='payment_details')