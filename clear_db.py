from app import create_app
from models import db

app = create_app() # Create the app instance

with app.app_context():
    db.drop_all()
    db.create_all()
    print("Database tables dropped and recreated successfully.")