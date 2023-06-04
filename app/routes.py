from flask import Flask, jsonify
from app import app

@app.route('/')
def index():
    return jsonify({"message":"Welcome to my site"})

