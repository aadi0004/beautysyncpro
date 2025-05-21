from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from ..models.salon import Salon
from ..models.appointment import Appointment, Service
from ..services.scheduler import suggest_slots
from .. import db
from datetime import datetime

bp = Blueprint('booking', __name__)

@bp.route('/book', methods=['GET', 'POST'])
def book():
    if 'user_id' not in session:
        flash('Please log in to book an appointment.', 'error')
        return redirect(url_for('auth.login'))
    
    user_id = session['user_id']
    salons = Salon.query.all()
    services = Service.query.all()
    
    user_appointments = Appointment.query.filter_by(user_id=user_id).all()
    
    if request.method == 'POST':
        salon_id = int(request.form['salon_id'])
        service_id = int(request.form['service_id'])
        slot = request.form['slot']
        start_time = datetime.strptime(slot, '%Y-%m-%d %H:%M:%S')
        
        available_slots = suggest_slots(salon_id, service_id)
        slot_available = False
        for date, slots in available_slots:
            if start_time in slots:
                slot_available = True
                break
        
        if slot_available:
            appointment = Appointment(user_id=user_id, salon_id=salon_id, service_id=service_id, start_time=start_time)
            db.session.add(appointment)
            db.session.commit()
            flash('Appointment booked successfully!', 'success')
            return redirect(url_for('booking.book'))
        else:
            flash('Selected time slot is not available.', 'error')
    
    available_slots = []
    if salons and services:
        available_slots = suggest_slots(salons[0].id, services[0].id)
    
    return render_template('booking.html', salons=salons, services=services, available_slots=available_slots, user_appointments=user_appointments)