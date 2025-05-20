from .. import db  # Relative import
from datetime import datetime

class Service(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    duration = db.Column(db.Integer, nullable=False)  # Duration in minutes
    salon_id = db.Column(db.Integer, db.ForeignKey('salon.id'), nullable=False)

class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    salon_id = db.Column(db.Integer, db.ForeignKey('salon.id'), nullable=False)
    service_id = db.Column(db.Integer, db.ForeignKey('service.id'), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(20), default='pending')
    user = db.relationship('User', backref='appointments')
    service = db.relationship('Service', backref='appointments')