from .. import db

class Salon(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    vendor_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)  # New field
    services = db.relationship('Service', backref='salon', lazy=True)
    appointments = db.relationship('Appointment', backref='salon', lazy=True)