from flask import Blueprint, render_template, request
from ..models.appointment import Appointment
from ..models.salon import Salon
from datetime import datetime, timedelta

bp = Blueprint('admin', __name__)

@bp.route('/dashboard')
def dashboard():
    # Get date filter from query parameter (default to today)
    date_str = request.args.get('date', datetime(2025, 5, 20).strftime('%Y-%m-%d'))
    try:
        filter_date = datetime.strptime(date_str, '%Y-%m-%d')
    except ValueError:
        filter_date = datetime(2025, 5, 20)
    
    next_date = filter_date + timedelta(days=1)
    
    # Fetch appointments for the selected date
    appointments = Appointment.query.filter(
        Appointment.start_time >= filter_date,
        Appointment.start_time < next_date
    ).all()
    
    salons = Salon.query.all()
    return render_template('dashboard.html', appointments=appointments, salons=salons, filter_date=filter_date)