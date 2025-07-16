from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from models import db, Movie, Person
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///media.db'
app.config['JWT_SECRET_KEY'] = 'supersecret'
CORS(app)

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

@app.route('/movies', methods=['GET'])
# @jwt_required()
def search_movies():
    query = Movie.query

    year = request.args.get('year')
    genre = request.args.get('genre')
    type_ = request.args.get('type')
    person_name = request.args.get('person_name')

    if year:
        query = query.filter(Movie.year_released == int(year))
    if genre:
        query = query.filter(Movie.genre.ilike(f"%{genre}%"))
    if type_:
        query = query.filter(Movie.type.ilike(f"%{type_}%"))
    if person_name:
        query = query.join(Movie.known_by).filter(Person.name.ilike(f"%{person_name}%"))

    results = []
    for movie in query.all():
        results.append({
            "Title": movie.title,
            "Year Released": movie.year_released,
            "Type": movie.type,
            "Genre": movie.genre,
            "List of People Associated": [p.name for p in movie.known_by]
        })

    return jsonify(results)

@app.route('/people', methods=['GET'])
# @jwt_required()
def search_people():
    query = Person.query

    name = request.args.get('name')
    profession = request.args.get('profession')
    movie_title = request.args.get('movie_title')

    if name:
        query = query.filter(Person.name.ilike(f"%{name}%"))
    if profession:
        query = query.filter(Person.profession.ilike(f"%{profession}%"))
    if movie_title:
        query = query.join(Person.known_for).filter(Movie.title.ilike(f"%{movie_title}%"))

    results = []
    for person in query.all():
        results.append({
            "Name": person.name,
            "Birth Year": person.birth_year,
            "Profession": person.profession,
            "Known for Titles": [m.title for m in person.known_for]
        })

    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)
