from app import db
from flask_login import UserMixin
from sqlalchemy.schema import Index
class Pet(db.Model):
    __tablename__ = 'pets'

    id = db.Column(db.Integer, primary_key = True)
    pet_name = db.Column(db.String(100), nullable = False)
    pet_type = db.Column(db.String(100), nullable = False)
    pet_age = db.Column(db.Integer(), nullable = False)
    pet_description = db.Column(db.String(100), nullable = False)

    def __repr__(self):
        return "<Pet %r, age %d, type %r, >" %self.pet_name, self.pet_age, self.pet_type
    
class User(db.Model, UserMixin):
    __tablename__='users'
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable = False)
    email = db.Column(db.String(60), nullable = False)
    password = db.Column(db.String(80), nullable = False)
    def get_id(self):
           return (self.user_id)
    def __repr__(self):
        return "<User %r>", self.username

Index('user_index', User.username, User.email)