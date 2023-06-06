
from flask import jsonify, request, abort, redirect, url_for
from app import app, db, bcrypt
from app.models import Pet, User
from flask_cors import cross_origin
from flask_login import login_user
from sqlalchemy import or_

@app.route('/')
def index():
    return jsonify({"message":"Welcome to my site"})

@cross_origin()
@app.route('/pets', methods=['POST'])
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

@cross_origin
@app.route('/pets',methods=['GET'])
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
        {
            "success":True,
            "pets":all_pets,
            "total_pets":len(pets),
        }
    )

@cross_origin
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
    
@cross_origin
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
    



@app.route('/login', methods = ['GET', 'POST'])
def login():
    '''
    Parses login information from json request. Aceepts both username or password. Returns a Json response 
    with the logged in state (true or false) and reason for failed attempts
    ''' 
    json_request = request.json
    
    user = User.query.filter(or_(User.username == json_request.get('username'), User.email == json_request.get('email'))).first()
    
    if user:
        if user.password==json_request['password']:
            login_user(user)
            return jsonify({"Logged in": True})
        return jsonify({"Logged in": False, "response": "Invalid password"})
    return jsonify({"Logged in":False, "response":"Invalid username"})
    