from flask import render_template, redirect, url_for, flash, request
from lostandfound_app import app, db  # ✅ you can safely import app here

from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

# ✅ Use only db import here
from lostandfound_app import db
from lostandfound_app.models import User, Item




@app.route('/')
def home():
    return render_template('index.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        roll_number = request.form['roll_no']
        email = request.form['email']
        password = generate_password_hash(request.form['password'])

        if User.query.filter_by(email=email).first():
            flash('Email already registered.')
            return redirect(url_for('signup'))

        user = User(name=name, roll_number=roll_number, email=email, password=password)
        db.session.add(user)
        db.session.commit()
        flash('Signup successful. Please log in.')
        return redirect(url_for('login'))

    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid credentials.')
            return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully.')
    return redirect(url_for('home'))

@app.route('/dashboard')
@login_required
def dashboard():
    items = Item.query.filter_by(user_id=current_user.id).all()
    return render_template('dashboard.html', items=items)
@app.route('/post', methods=['GET', 'POST'])
@login_required
def post_item():
    if request.method == 'POST':
        item_name = request.form['item_name']
        item_type = request.form['item_type']
        description = request.form['description']
        status = request.form['status']
        branch = request.form['branch']

        new_item = Item(
            item_name=item_name,
            item_type=item_type,
            description=description,
            status=status,
            branch=branch,
            user_id=current_user.id,
            student_name=current_user.name,
            roll_number=current_user.roll_number
        )

        db.session.add(new_item)
        db.session.commit()
        flash('Item posted successfully!', 'success')
        return redirect(url_for('dashboard'))

    return render_template('post_item.html')


@app.route('/items')
def view_items():
    items = Item.query.all()
    return render_template('view_items.html', items=items)

@app.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form['email']
        new_password = request.form['new_password']
        user = User.query.filter_by(email=email).first()
        if user:
            user.password = generate_password_hash(new_password)
            db.session.commit()
            flash('Password reset successfully.', 'success')
            return redirect(url_for('login'))
        else:
            flash('User not found.', 'danger')
    return render_template('forgot_password.html')
