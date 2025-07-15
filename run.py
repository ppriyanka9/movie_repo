# run.py
from app import create_app, db
from app.models import User

app = create_app()

# Create tables before first request
@app.before_first_request
def create_tables():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
