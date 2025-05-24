import sys
import os
import time
from datetime import datetime
from sqlalchemy.exc import OperationalError
from sqlalchemy.sql import text
from backend.app import create_app, db
from flask_migrate import Migrate, upgrade
from backend.app.models.user import User
from backend.app.models.salon import Salon
from backend.app.models.appointment import Service, Appointment

sys.path.append(os.path.abspath(os.path.dirname(__file__)))

app = create_app()
migrate = Migrate(app, db)

def wait_for_db():
    """Wait for the database to be ready with retries."""
    retries = 10
    delay = 5  # seconds
    for i in range(retries):
        try:
            with app.app_context():
                # Test the connection by querying the database
                db.session.execute(text('SELECT 1'))
                db.session.commit()
            print("Database connection successful!")
            return True
        except OperationalError as e:
            print(f"Database connection failed: {e}. Retrying in {delay} seconds... ({i+1}/{retries})")
            time.sleep(delay)
        except Exception as e:
            print(f"Unexpected error while connecting to database: {e}. Retrying in {delay} seconds... ({i+1}/{retries})")
            time.sleep(delay)
    print("Failed to connect to the database after multiple attempts.")
    return False

def ensure_tables():
    """Ensure all tables are created if migrations fail or aren't available."""
    with app.app_context():
        try:
            # Check if the 'user' table exists
            result = db.session.execute(text("SHOW TABLES LIKE 'user'")).fetchall()
            if not result:
                print("Tables not found. Creating tables...")
                db.create_all()  # Create all tables defined in models
                print("Tables created successfully.")
            else:
                print("Tables already exist.")
        except Exception as e:
            print(f"Error while ensuring tables: {e}")
            raise

def seed_database():
    """Seed the database with initial data."""
    try:
        # Superuser creation
        superuser_email = 'aditya768888@gmail.com'
        superuser = User.query.filter_by(email=superuser_email).first()
        if not superuser:
            superuser = User(
                username='aditya_superuser',
                email=superuser_email,
                user_type='vendor',
                is_admin=True
            )
            superuser.set_password('aditya230f')
            db.session.add(superuser)
            db.session.commit()
        else:
            superuser.is_admin = True
            superuser.set_password('aditya230f')
            db.session.commit()

        # Ensure only superuser is admin
        User.query.filter((User.email != superuser_email) & (User.is_admin == True)).update({'is_admin': False})
        db.session.commit()

        # Seed users if none exist (excluding superuser)
        if User.query.filter(User.email != superuser_email).count() == 0:
            users = [
                ('alice', 'alice@example.com', 'customer'),
                ('bob', 'bob@example.com', 'customer'),
                ('charlie', 'charlie@example.com', 'customer'),
                ('diana', 'diana@example.com', 'customer'),
                ('eve', 'eve@example.com', 'customer'),
                ('vendor1', 'vendor1@example.com', 'vendor'),
                ('vendor2', 'vendor2@example.com', 'vendor'),
                ('vendor3', 'vendor3@example.com', 'vendor'),
                ('vendor4', 'vendor4@example.com', 'vendor'),
                ('vendor5', 'vendor5@example.com', 'vendor'),
            ]
            for username, email, user_type in users:
                user = User(username=username, email=email, user_type=user_type)
                user.set_password('password123')
                db.session.add(user)
            db.session.commit()

        # Seed salons
        if not Salon.query.first():
            vendors = User.query.filter_by(user_type='vendor').filter(User.email != superuser_email).all()
            vendor_ids = [vendor.id for vendor in vendors]
            salons = [
                ('Glow Haven Spa', '123 Main St, Mumbai', vendor_ids[0]),
                ('Radiance Salon', '456 Oak Ave, Delhi', vendor_ids[1]),
                ('Bliss Beauty Lounge', '789 Pine Rd, Bangalore', vendor_ids[2]),
                ('Serene Spa', '101 Maple Dr, Chennai', vendor_ids[3]),
                ('Elegance Salon', '202 Cedar Ln, Hyderabad', vendor_ids[4]),
                ('Tranquil Touch', '303 Birch St, Pune', vendor_ids[0]),
                ('Luxe Beauty Studio', '404 Elm Ave, Kolkata', vendor_ids[1]),
                ('Harmony Spa', '505 Willow Rd, Ahmedabad', vendor_ids[2]),
                ('Chic Salon', '606 Ash Dr, Jaipur', vendor_ids[3]),
                ('Vogue Wellness', '707 Spruce Ln, Surat', vendor_ids[4]),
            ]
            for name, address, vendor_id in salons:
                db.session.add(Salon(name=name, address=address, vendor_id=vendor_id))
            db.session.commit()

        # Seed services
        if not Service.query.first():
            services = [
                ('Facial', 60, 1),
                ('Haircut', 45, 1),
                ('Manicure', 30, 2),
                ('Pedicure', 40, 2),
                ('Massage', '90', 3),
                ('Hair Coloring', 120, 4),
                ('Waxing', 30, 5),
                ('Eyebrow Threading', 15, 6),
                ('Makeup', 60, 7),
                ('Nail Art', 45, 8),
            ]
            for name, duration, salon_id in services:
                db.session.add(Service(name=name, duration=duration, salon_id=salon_id))
            db.session.commit()

        # Seed appointments
        if not Appointment.query.first():
            appointments = [
                (1, 1, 1, datetime(2025, 5, 20, 19, 0), 'confirmed'),
                (2, 1, 2, datetime(2025, 5, 20, 19, 30), 'pending'),
                (3, 2, 3, datetime(2025, 5, 21, 9, 0), 'confirmed'),
                (4, 2, 4, datetime(2025, 5, 21, 10, 0), 'pending'),
                (5, 3, 5, datetime(2025, 5, 21, 11, 0), 'confirmed'),
                (1, 4, 6, datetime(2025, 5, 21, 13, 0), 'pending'),
                (2, 5, 7, datetime(2025, 5, 22, 9, 0), 'confirmed'),
                (3, 6, 8, datetime(2025, 5, 22, 10, 0), 'pending'),
                (4, 7, 9, datetime(2025, 5, 22, 11, 0), 'confirmed'),
                (5, 8, 10, datetime(2025, 5, 22, 12, 0), 'pending'),
            ]
            for user_id, salon_id, service_id, start_time, status in appointments:
                db.session.add(Appointment(user_id=user_id, salon_id=salon_id, service_id=service_id, start_time=start_time, status=status))
            db.session.commit()
        print("Database seeding completed successfully.")
    except Exception as e:
        print(f"Error during seeding: {e}")
        db.session.rollback()
        raise

# Wait for the database to be ready, then apply migrations and seed
if wait_for_db():
    with app.app_context():
        try:
            print("Applying database migrations...")
            upgrade()  # Apply migrations safely
            print("Database migrations applied successfully.")
            ensure_tables()  # Ensure tables exist as a fallback
            seed_database()  # Seed the database after migrations
        except Exception as e:
            print(f"Error during migrations or seeding: {e}")
            raise
else:
    raise Exception("Cannot proceed without a database connection.")

# Add a test route to verify the backend is running
@app.route('/health')
def health_check():
    return "Backend is running!", 200

if __name__ == '__main__':
    if os.getenv('FLASK_ENV') == 'production':
        pass  # Let Gunicorn handle it
    else:
        app.run(debug=True, host='0.0.0.0', port=5000)