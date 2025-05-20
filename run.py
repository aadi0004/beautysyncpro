import sys
import os
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from backend.app import create_app, db
from backend.app.models.user import User
from backend.app.models.salon import Salon
from backend.app.models.appointment import Service

app = create_app()

with app.app_context():
    # Check if tables are empty before seeding
    if not Salon.query.first() and not Service.query.first():
        salon = Salon(name="BeautyBliss Spa", address="123 Mumbai St")
        db.session.add(salon)
        db.session.commit()
        service = Service(name="Facial", duration=60, salon_id=salon.id)
        db.session.add(service)
        db.session.commit()

if __name__ == '__main__':
    app.run(debug=True)