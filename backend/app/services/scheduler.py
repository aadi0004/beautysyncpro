from datetime import datetime, timedelta
from ..models.appointment import Appointment, Service
from .. import db

def suggest_slots(salon_id, service_id, start_date=None):
    # Use current date if none provided (May 20, 2025)
    if start_date is None:
        start_date = datetime(2025, 5, 20)  # Hardcoded for now; in production, use datetime.now()
    
    # Suggest slots for the next 3 days
    service = Service.query.get(service_id)
    duration = service.duration
    
    all_slots = []
    for day in range(3):  # Next 3 days: May 20, 21, 22
        current_date = start_date + timedelta(days=day)
        end_date = current_date + timedelta(days=1)
        
        # Get existing appointments for the salon on the date
        appointments = Appointment.query.filter(
            Appointment.salon_id == salon_id,
            Appointment.start_time >= current_date,
            Appointment.start_time < end_date
        ).all()
        
        # Generate available slots (9 AM to 6 PM, every 30 minutes)
        slots = []
        current_time = current_date.replace(hour=9, minute=0)
        # For May 20, start from the current time (06:36 PM IST)
        if day == 0:
            current_hour = 18  # 06:36 PM IST
            current_minute = 36
            if current_hour > 9 or (current_hour == 9 and current_minute > 0):
                current_time = current_date.replace(hour=current_hour, minute=current_minute)
        
        while current_time < current_date.replace(hour=18, minute=0):
            slot_end = current_time + timedelta(minutes=duration)
            if not any(
                app.start_time <= current_time < app.start_time + timedelta(minutes=Service.query.get(app.service_id).duration)
                for app in appointments
            ):
                slots.append(current_time)
            current_time += timedelta(minutes=30)
        
        all_slots.append((current_date, slots))
    
    return all_slots