import csv
from flask import Flask
from models import db, Movie, Person
from app import app

def import_movies():
    with open('data/title.basics.tsv', newline='', encoding='utf-8') as tsvfile:
        reader = csv.DictReader(tsvfile, delimiter='\t')
        for row in reader:
            if row['titleType'] not in ('movie', 'tvMovie', 'short'):
                continue
            movie = Movie(
                id=row['tconst'],
                title=row['primaryTitle'],
                year_released=int(row['startYear']) if row['startYear'].isdigit() else None,
                type=row['titleType'],
                genre=row['genres']
            )
            db.session.merge(movie)
    db.session.commit()

def import_people():
    with open('data/name.basics.tsv', newline='', encoding='utf-8') as tsvfile:
        reader = csv.DictReader(tsvfile, delimiter='\t')
        for row in reader:
            person = Person(
                        id=row['nconst'],
                        name=row['primaryName'],
                        birth_year=int(row['birthYear']) if row['birthYear'].isdigit() else None,
                        death_year=int(row['deathYear']) if row['deathYear'].isdigit() else None,
                        profession=row['primaryProfession']
                    )

            db.session.add(person)  # Add person to session early

            # Link knownForTitles
            known_titles = row['knownForTitles'].split(',') if row['knownForTitles'] != '\\N' else []
            for title_id in known_titles:
                movie = db.session.get(Movie, title_id)
                if movie:
                    person.known_for.append(movie)


def run_import():
    with app.app_context():
        db.create_all()
        import_movies()
        import_people()
        db.session.commit()
        print("TSV data import completed successfully.")

if __name__ == '__main__':
    run_import()
