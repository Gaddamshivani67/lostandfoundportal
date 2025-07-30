# setup_db.py

from lostandfound_app import app, db

with app.app_context():
    db.create_all()
    print("✅ Database and all tables created successfully!")
