from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from ..models.appointment import Appointment
from ..models.user import User
from .. import db
from datetime import datetime

bp = Blueprint('customer', __name__)

@bp.route('/customer/dashboard')
def dashboard():
    if 'user_id' not in session:
        flash('Please log in to access your dashboard.', 'error')
        return redirect(url_for('auth.login'))
    
    user = db.session.get(User, session['user_id'])
    if not user or user.user_type != 'customer':
        flash('Access denied. Customer login required.', 'error')
        return redirect(url_for('auth.index'))
    
    # Fetch all appointments for the customer, ordered by start time
    appointments = Appointment.query.filter_by(user_id=user.id).order_by(Appointment.start_time.asc()).all()
    
    return render_template('customer_dashboard.html', appointments=appointments, current_time=datetime.now())

@bp.route('/customer/cancel/<int:appointment_id>')
def cancel_appointment(appointment_id):
    if 'user_id' not in session:
        flash('Please log in to perform this action.', 'error')
        return redirect(url_for('auth.login'))
    
    user = db.session.get(User, session['user_id'])
    if not user or user.user_type != 'customer':
        flash('Access denied. Customer login required.', 'error')
        return redirect(url_for('auth.index'))
    
    appointment = Appointment.query.get_or_404(appointment_id)
    
    # Check if the appointment belongs to the customer
    if appointment.user_id != user.id:
        flash('Access denied. You can only cancel your own appointments.', 'error')
        return redirect(url_for('customer.dashboard'))
    
    # Check if the appointment is in the future and has a cancellable status
    current_time = datetime.now()
    if appointment.start_time <= current_time:
        flash('Cannot cancel past appointments.', 'error')
        return redirect(url_for('customer.dashboard'))
    
    if appointment.status not in ['pending', 'confirmed']:
        flash('Cannot cancel an appointment that is already declined or cancelled.', 'error')
        return redirect(url_for('customer.dashboard'))
    
    # Update the appointment status to 'cancelled'
    appointment.status = 'cancelled'
    db.session.commit()
    flash('Appointment cancelled successfully.', 'success')
    return redirect(url_for('customer.dashboard'))