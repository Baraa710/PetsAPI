from flask import jsonify, request, abort, make_response, Response
from app import app, db, bcrypt, login_manager
from app.models import Pet, User
from flask_login import login_user, login_required, logout_user, current_user
from sqlalchemy import or_
from app.auth import *

@login_manager.user_loader
def load_user(user_id):
    '''takes in user id and returns the user from the database'''
    return User.query.get(int(user_id))
@app.route('/')
def index():
    return jsonify({"message":"Welcome to my site"})


@app.route('/pets', methods=['POST'])
@login_required
def create_pet():
    """"""
    pet_data = request.json

    pet_name = pet_data['pet_name']
    pet_type = pet_data['pet_type']
    pet_age = pet_data['pet_age']
    pet_description = pet_data['pet_description']
    # pet=Pet(**pet_data)
    pet = Pet(pet_name =pet_name , pet_type = pet_type, pet_age = pet_age, pet_description =pet_description)
    db.session.add(pet)
    db.session.commit()

    return jsonify({"success":True, "response":"Pet "+pet_name+" added" })


@app.route('/pets',methods=['GET'])
@login_required
def getpets():
    """Returns a json string containing all pets in the database"""
    all_pets = []
    pets = Pet.query.all()
    for pet in pets:
        results = {
            "pet_id":pet.id,
            "pet_name":pet.pet_name,
            "pet_age":pet.pet_age,
            "pet_type":pet.pet_type,
            "pet_description":pet.pet_description,
        }

        all_pets.append(results)
    
    return jsonify(
        {   "username" : current_user.username,
            "success":True,
            "pets":all_pets,
            "total_pets":len(pets),
        }
    )

@login_required
@app.route("/pets/<int:pet_id>", methods = ["PATCH"])
def update_pet(pet_id):
    """Takes pet id, update a pet age and/or description."""
    pet = Pet.query.get(pet_id)
    json_request = request.json

    if pet is None:
        abort(404)

    else:
        if "pet_age" in json_request:
            pet.pet_age = request.json['pet_age']
        if "pet_description" in json_request:
            pet.pet_description = request.json['pet_description']
        db.session.add(pet)
        db.session.commit()
        return jsonify({"success": True, "response": "Pet Details updated"})
    
@login_required
@app.route("/pets/<int:pet_id>", methods = ["DELETE"])
def delete_pet(pet_id):
    """given pet id, this function removes the pet from the database"""
    pet = Pet.query.get(pet_id)
    if pet is None:
        abort(404)
    else:
        db.session.delete(pet)
        db.session.commit()
        return jsonify({"success": True, "response": "Pet with id " +str(pet_id) +" deleted"})
    



@app.route('/login', methods = ['POST'])
def login():
    '''
    Parses login information from json request. Aceepts both username or email. Returns a Json response 
    with the logged in state (true or false) and reason for failed attempts
    ''' 
    json_request = request.json
    username = json_request.get('username')
    email = json_request.get('email')
    password = json_request.get('password')
    if not (email or username) or not password:
        return jsonify({"Response": "Missing information"}), 400
    user = User.query.filter(or_(User.username == username, User.email == email)).first()
    
    if user:
        if bcrypt.check_password_hash(user.password, json_request.get('password') ):
            login_user(user)
            return jsonify({"Logged in": True, "username" : current_user.username})
        response = make_response("<h1>Failure</h1>")
        response.status_code = 401
        return jsonify({'logged in':False}), 401
    return jsonify({'logged in':False}), 401

@login_required
@app.route('/logout', methods= ['GET', 'POST'])
def logout():
    '''Handles logging out and directs to login page'''
    logout_user()
    return jsonify({"Logged in":False}) , 401

@app.route('/register', methods = ['POST'])
def register():
    json_request = request.json

    hashed_password = bcrypt.generate_password_hash(json_request.get('password'))
    hashed_password = hashed_password.decode("utf-8", "ignore")
    username = json_request.get('username')
    email = json_request.get('email')
    if not email or not username or not hashed_password:
        return jsonify({"Response": "Missing information"}), 400
    if len(username)<5:
        return jsonify({"Response":"Username is too short"}), 401
    elif len(username)>20:
        return jsonify({"Response":"Username is too long"}), 401
    
    if not is_valid_email_address(email):
        return jsonify({"Response":"Invalid email address"}), 401


    user = User.query.filter(User.email == email).first()
    if user:
        return jsonify({"Response":"email address already used"}), 401
    user = User.query.filter(User.username == username).first()
    if user:
        return jsonify({"Response":"username already used"}), 401
    new_user = User(username = username, email = email, password = hashed_password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"New User": True})