from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from ..models.user import User
from .. import db

bp = Blueprint('auth', __name__)

@bp.route('/')
def index():
    # Fetch all salons to display on homepage
    from ..models.salon import Salon
    salons = Salon.query.all()
    # Check if user is logged in
    user = None
    if 'user_id' in session:
        user = User.query.get(session['user_id'])
    return render_template('index.html', salons=salons, user=user)

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already registered.', 'error')
            return redirect(url_for('auth.register'))
        new_user = User(username=username, email=email)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('auth.login'))
    return render_template('index.html')

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            session['user_id'] = user.id  # Store user ID in session
            flash('Login successful!', 'success')
            return redirect(url_for('booking.book'))
        flash('Invalid email or password.', 'error')
    return render_template('index.html')

@bp.route('/logout')
def logout():
    session.pop('user_id', None)  # Remove user ID from session
    flash('Logged out successfully.', 'success')
    return redirect(url_for('auth.index'))