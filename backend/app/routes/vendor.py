from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from ..models.appointment import Appointment
from ..models.salon import Salon
from ..models.user import User
from ..models.appointment import Service
from .. import db, mail
from flask_mail import Message

bp = Blueprint('vendor', __name__)

@bp.route('/vendor/add-salon-services', methods=['GET', 'POST'])
def add_salon_services():
    if 'user_id' not in session:
        flash('Please log in to access this page.', 'error')
        return redirect(url_for('auth.login'))
    
    user = db.session.get(User, session['user_id'])
    if not user or user.user_type != 'vendor':
        flash('Access denied. Vendor login required.', 'error')
        return redirect(url_for('auth.index'))
    
    # Check if the vendor already has a salon
    existing_salon = Salon.query.filter_by(vendor_id=user.id).first()
    if existing_salon:
        flash('You have already added a salon. Please contact the superuser to add another.', 'info')
        return redirect(url_for('vendor.dashboard'))
    
    if request.method == 'POST':
        # Salon details
        salon_name = request.form.get('salon_name')
        salon_address = request.form.get('salon_address')
        
        # Service details (allow multiple services)
        service_names = request.form.getlist('service_name')
        service_durations = request.form.getlist('service_duration')
        
        # Validate salon details
        if not salon_name or not salon_address:
            flash('Salon name and address are required.', 'error')
            return redirect(url_for('vendor.add_salon_services'))
        
        # Validate services
        if not service_names or not service_durations or len(service_names) != len(service_durations):
            flash('At least one service is required with a valid name and duration.', 'error')
            return redirect(url_for('vendor.add_salon_services'))
        
        services = []
        for name, duration in zip(service_names, service_durations):
            if not name or not duration:
                flash('Service name and duration cannot be empty.', 'error')
                return redirect(url_for('vendor.add_salon_services'))
            try:
                duration = int(duration)
                if duration <= 0:
                    flash('Service duration must be a positive number.', 'error')
                    return redirect(url_for('vendor.add_salon_services'))
            except ValueError:
                flash('Service duration must be a valid number.', 'error')
                return redirect(url_for('vendor.add_salon_services'))
            services.append({'name': name, 'duration': duration})
        
        # Add the salon
        new_salon = Salon(name=salon_name, address=salon_address, vendor_id=user.id)
        db.session.add(new_salon)
        db.session.flush()  # Flush to get the salon ID
        
        # Add the services
        for service in services:
            new_service = Service(name=service['name'], duration=service['duration'], salon_id=new_salon.id)
            db.session.add(new_service)
        
        db.session.commit()
        
        flash('Salon and services added successfully! You can now manage appointments.', 'success')
        return redirect(url_for('vendor.dashboard'))
    
    return render_template('add_salon_services.html')

@bp.route('/vendor')
def dashboard():
    if 'user_id' not in session:
        flash('Please log in to access the vendor dashboard.', 'error')
        return redirect(url_for('auth.login'))
    
    user = db.session.get(User, session['user_id'])
    if not user or user.user_type != 'vendor':
        flash('Access denied. Vendor login required.', 'error')
        return redirect(url_for('auth.index'))
    
    salons = Salon.query.filter_by(vendor_id=user.id).all()
    salon_ids = [salon.id for salon in salons]
    
    appointments = Appointment.query.filter(
        Appointment.salon_id.in_(salon_ids)
    ).order_by(Appointment.start_time.asc()).all()
    
    return render_template('vendor.html', appointments=appointments, salons=salons)

@bp.route('/vendor/accept/<int:appointment_id>')
def accept_appointment(appointment_id):
    if 'user_id' not in session:
        flash('Please log in to perform this action.', 'error')
        return redirect(url_for('auth.login'))
    
    user = db.session.get(User, session['user_id'])
    if not user or user.user_type != 'vendor':
        flash('Access denied. Vendor login required.', 'error')
        return redirect(url_for('auth.index'))
    
    appointment = Appointment.query.get_or_404(appointment_id)
    salon = Salon.query.get(appointment.salon_id)
    if salon.vendor_id != user.id:
        flash('Access denied. You do not own this salon.', 'error')
        return redirect(url_for('vendor.dashboard'))
    
    appointment.status = 'confirmed'
    db.session.commit()
    
    customer = appointment.user
    msg = Message(
        subject='Appointment Confirmation - BeautySyncPro',
        recipients=[customer.email],
        body=f"""
        Dear {customer.username},

        Your appointment has been confirmed!

        Details:
        - Salon: {appointment.salon.name}
        - Service: {appointment.service.name}
        - Date and Time: {appointment.start_time.strftime('%Y-%m-%d %H:%M')}
        - Status: Confirmed

        We look forward to serving you!

        Best regards,
        BeautySyncPro Team
        """
    )
    try:
        mail.send(msg)
        flash('Appointment confirmed! Confirmation email sent to the customer.', 'success')
    except Exception as e:
        flash('Appointment confirmed, but failed to send email: ' + str(e), 'warning')
    
    return redirect(url_for('vendor.dashboard'))

@bp.route('/vendor/decline/<int:appointment_id>')
def decline_appointment(appointment_id):
    if 'user_id' not in session:
        flash('Please log in to perform this action.', 'error')
        return redirect(url_for('auth.login'))
    
    user = db.session.get(User, session['user_id'])
    if not user or user.user_type != 'vendor':
        flash('Access denied. Vendor login required.', 'error')
        return redirect(url_for('auth.index'))
    
    appointment = Appointment.query.get_or_404(appointment_id)
    salon = Salon.query.get(appointment.salon_id)
    if salon.vendor_id != user.id:
        flash('Access denied. You do not own this salon.', 'error')
        return redirect(url_for('vendor.dashboard'))
    
    appointment.status = 'declined'
    db.session.commit()
    flash('Appointment declined.', 'success')
    return redirect(url_for('vendor.dashboard'))