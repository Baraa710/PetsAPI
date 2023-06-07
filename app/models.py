from app import db
from flask_login import UserMixin
from sqlalchemy.schema import Index, CheckConstraint
class Pet(db.Model):
    __tablename__ = 'pets'

    id = db.Column(db.Integer, primary_key = True)
    pet_name = db.Column(db.String(100), nullable = False)
    pet_type = db.Column(db.String(100), nullable = False)
    pet_age = db.Column(db.Integer(), nullable = False)
    pet_description = db.Column(db.String(100), nullable = False)

    def __repr__(self):
        return "<Pet %r, age %d, type %r, >" %self.pet_name, self.pet_age, self.pet_type


def string_column(name, min_length, max_length):
    check_str = "LENGTH({}) < {}".format(name, max_length) + "LENGTH({}) > {}".format(name, min_length)
    return db.Column(name, db.String(max_length), CheckConstraint(check_str), nullable = False)   

class User(db.Model, UserMixin):
    __tablename__='users'
    user_id = db.Column(db.Integer, primary_key=True)
    username = string_column('username', 6, 20)
    email = string_column('email',3,320)
    password = string_column('password',6,300)
    def get_id(self):
           return (self.user_id)
    def __repr__(self):
        return "<User %r>", self.username

Index('user_index', User.username, User.email)