# app/routes.py
from flask import Blueprint, jsonify
from .models import User
from . import db

main = Blueprint('main', __name__)

@main.route('/')
def home():
    return "Flask app with DB!"

@main.route('/users')
def list_users():
    users = User.query.all()
    return jsonify([{'id': u.id, 'name': u.name} for u in users])
