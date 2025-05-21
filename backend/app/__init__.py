from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_mail import Mail
from .config import Config

db = SQLAlchemy()
migrate = Migrate()
mail = Mail()

def create_app():
    app = Flask(__name__, template_folder='../../frontend', static_folder='../../frontend/assets')
    app.config.from_object(Config)
    
    db.init_app(app)
    migrate.init_app(app, db)
    mail.init_app(app)
    
    from .routes import auth, booking, admin, vendor, customer, superuser
    app.register_blueprint(auth)
    app.register_blueprint(booking)
    app.register_blueprint(admin)
    app.register_blueprint(vendor)
    app.register_blueprint(customer)
    app.register_blueprint(superuser)
    
    return app