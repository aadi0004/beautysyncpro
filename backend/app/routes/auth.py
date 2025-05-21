from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from ..models.user import User
from .. import db

bp = Blueprint('auth', __name__)

@bp.route('/')
def index():
    from ..models.salon import Salon
    salons = Salon.query.all()
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
        user_type = request.form.get('user_type', 'customer')
        
        # Prevent admin registration unless the email is the superuser's
        superuser_email = 'aditya768888@gmail.com'
        is_admin = False
        if email == superuser_email:
            is_admin = True
        elif 'is_admin' in request.form and request.form['is_admin'] == 'on':
            flash('Admin registration is restricted to the superuser.', 'error')
            return redirect(url_for('auth.register'))
        
        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already registered.', 'error')
            return redirect(url_for('auth.register'))
        
        new_user = User(username=username, email=email, user_type=user_type, is_admin=is_admin)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        
        # Ensure no other users are admins
        if is_admin:
            User.query.filter(User.email != superuser_email, User.is_admin == True).update({'is_admin': False})
            db.session.commit()
        
        # Log the user in automatically after registration
        session['user_id'] = new_user.id
        
        # Redirect vendors to add salon and services
        if user_type == 'vendor':
            flash('Registration successful! Please add your salon and services.', 'success')
            return redirect(url_for('vendor.add_salon_services'))
        
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
            session['user_id'] = user.id
            flash('Login successful!', 'success')
            if user.is_admin:
                return redirect(url_for('superuser.add_salon'))
            elif user.user_type == 'vendor':
                return redirect(url_for('vendor.dashboard'))
            else:
                return redirect(url_for('booking.book'))
        flash('Invalid email or password.', 'error')
    return render_template('index.html')

@bp.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('Logged out successfully.', 'success')
    return redirect(url_for('auth.index'))