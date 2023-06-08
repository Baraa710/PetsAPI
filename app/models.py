from app import db
from flask_login import UserMixin
from sqlalchemy.schema import Index, CheckConstraint
from sqlalchemy.orm import validates
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Pet(db.Model):
    __tablename__ = 'pets'

    id = db.Column(db.Integer, primary_key = True)
    pet_name = db.Column(db.String(100), nullable = False)
    pet_type = db.Column(db.String(100), nullable = False)
    pet_age = db.Column(db.Integer(), nullable = False)
    pet_description = db.Column(db.String(100), nullable = False)

    def __repr__(self):
        return "<Pet %r, age %d, type %r, >" %self.pet_name, self.pet_age, self.pet_type



class User(db.Model, UserMixin, Base):
    __tablename__='users'
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20),unique = True, nullable = False)
    email = db.Column(db.String(60),unique = True, nullable = False)
    password =  db.Column(db.String(100),unique = True, nullable = False)
    __table_args__ = (
        CheckConstraint('char_length(username)> 5',
                        name='some_string_min_length'),
    )
    @validates('username')
    def validate_some_string(self, key, username) -> str:
        if len(username) <= 5:
            raise ValueError('username too short')
        return username
    @validates('email')
    def validate_some_string(self, key, email) -> str:
        if len(email) <= 2:
            raise ValueError('email too short')
        return email
    
    

    def get_id(self):
           return (self.user_id)
    def __repr__(self):
        return "<User %r>", self.username

Index('user_index', User.username, User.email)