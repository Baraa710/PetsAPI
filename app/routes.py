
from flask import jsonify, request
from app import app, db
from app.models import Pet
from flask_cors import cross_origin


@app.route('/')
def index():
    return jsonify({"message":"Welcome to my site"})

@cross_origin()
@app.route('/pets', methods=['POST'])
def create_pet():
    pet_data = request.json

    pet_name = pet_data['pet_name']
    pet_type = pet_data['pet_type']
    pet_age = pet_data['pet_age']
    pet_description = pet_data['pet_description']

    pet = Pet(pet_name =pet_name , pet_type = pet_type, pet_age = pet_age, pet_description =pet_description)
    db.session.add(pet)
    db.session.commit()

    return jsonify({"success":True, "response":"Pet  added"})