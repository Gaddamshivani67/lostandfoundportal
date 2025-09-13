from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# Initialize Flask app
app = Flask(__name__)

# Config
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///lostandfound.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

# Import routes and models AFTER initialization
from lostandfound_app import routes, models
from lostandfound_app.models import User  # add this line to import the User model

# ✅ Add the required user_loader callback
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
