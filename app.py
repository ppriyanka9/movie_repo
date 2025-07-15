from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from models import db, Movie, Person
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///media.db'
app.config['JWT_SECRET_KEY'] = 'supersecret'
db.init_app(app)
jwt = JWTManager(app)

# Dummy user
USERS = {
    "admin": "password123"
}

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    if USERS.get(username) == password:
        token = create_access_token(identity=username, expires_delta=datetime.timedelta(hours=1))
        return jsonify(access_token=token)
    return jsonify({"msg": "Bad credentials"}), 401
