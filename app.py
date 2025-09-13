from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

db = SQLAlchemy(app)

# User Loader for Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Database Models
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    rollno = db.Column(db.String(50), nullable=False)
    branch = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

# Routes
@app.route("/")
def home():
    return render_template("home.html")

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        name = request.form["name"]
        rollno = request.form["rollno"]
        branch = request.form["branch"]
        email = request.form["email"]
        password = generate_password_hash(request.form["password"], method="pbkdf2:sha256")

        if User.query.filter_by(email=email).first():
            flash("Email already registered!", "danger")
            return redirect(url_for("signup"))

        new_user = User(name=name, rollno=rollno, branch=branch, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()
        flash("Signup successful! Please log in.", "success")
        return redirect(url_for("login"))
    return render_template("signup.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for("dashboard"))
        else:
            flash("Invalid credentials, please try again.", "danger")
    return render_template("login.html")

@app.route("/dashboard")
@login_required
def dashboard():
    items = Item.query.all()
    return render_template("dashboard.html", items=items)

@app.route("/post_item", methods=["GET", "POST"])
@login_required
def post_item():
    if request.method == "POST":
        title = request.form["title"]
        description = request.form["description"]
        new_item = Item(title=title, description=description, user_id=current_user.id)
        db.session.add(new_item)
        db.session.commit()
        flash("Item posted successfully!", "success")
        return redirect(url_for("dashboard"))
    return render_template("post_item.html")

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("home"))
app=app

# ✅ For Vercel: Don't call app.run()
# Instead, expose app object
# app.run(debug=True) --> ❌ REMOVE this line
