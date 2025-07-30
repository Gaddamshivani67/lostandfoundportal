from lostandfound_app import app, db
from lostandfound_app.models import User
from lostandfound_app import bcrypt

def create_admin_user():
    with app.app_context():
        existing_admin = User.query.filter_by(username='admin').first()
        if existing_admin:
            print("⚠️ Admin user already exists.")
            return

        hashed_password = bcrypt.generate_password_hash('admin123').decode('utf-8')

        admin = User(
            username='admin',
            email='admin@vce.ac.in',
            password=hashed_password,
            name='Admin',
            roll_number='000',
            branch='Admin',
        )
        db.session.add(admin)
        db.session.commit()
        print("✅ Admin user created successfully.")

if __name__ == '__main__':
    create_admin_user()
