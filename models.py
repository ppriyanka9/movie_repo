from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

person_known_for = db.Table('person_known_for',
    db.Column('person_id', db.String, db.ForeignKey('person.id'), primary_key=True),
    db.Column('movie_id', db.String, db.ForeignKey('movie.id'), primary_key=True)
)

class Movie(db.Model):
    id = db.Column(db.String, primary_key=True)  # tconst
    title = db.Column(db.String)
    year_released = db.Column(db.Integer)
    type = db.Column(db.String)
    genre = db.Column(db.String)

    known_by = db.relationship('Person', secondary='person_known_for', back_populates='known_for')


class Person(db.Model):
    id = db.Column(db.String, primary_key=True)  # nconst
    name = db.Column(db.String)
    birth_year = db.Column(db.Integer)
    death_year = db.Column(db.Integer, nullable=True)
    profession = db.Column(db.String)

    known_for = db.relationship('Movie', secondary='person_known_for', back_populates='known_by')
