from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from ..models.salon import Salon
from ..models.user import User
from .. import db

bp = Blueprint('superuser', __name__)

@bp.route('/superuser/add-salon', methods=['GET', 'POST'])
def add_salon():
    if 'user_id' not in session:
        flash('Please log in to access this page.', 'error')
        return redirect(url_for('auth.login'))
    
    user = db.session.get(User, session['user_id'])
    if not user or not user.is_admin:
        flash('Access denied. Superuser privileges required.', 'error')
        return redirect(url_for('auth.index'))
    
    if request.method == 'POST':
        name = request.form.get('name')
        address = request.form.get('address')
        vendor_id = request.form.get('vendor_id')
        
        # Validate form inputs
        if not name or not address or not vendor_id:
            flash('All fields are required.', 'error')
            return redirect(url_for('superuser.add_salon'))
        
        # Validate vendor
        vendor = db.session.get(User, int(vendor_id))
        if not vendor or vendor.user_type != 'vendor':
            flash('Invalid vendor selected.', 'error')
            return redirect(url_for('superuser.add_salon'))
        
        # Add the new salon
        new_salon = Salon(name=name, address=address, vendor_id=vendor.id)
        db.session.add(new_salon)
        db.session.commit()
        
        flash(f'Salon "{name}" added successfully!', 'success')
        return redirect(url_for('superuser.add_salon'))
    
    # Fetch all vendors for the dropdown
    vendors = User.query.filter_by(user_type='vendor').all()
    return render_template('add_salon.html', vendors=vendors)