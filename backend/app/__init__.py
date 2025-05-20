from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from .config import Config  # Relative import of Config

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__, template_folder='../../frontend', static_folder='../../frontend/assets')
    app.config.from_object(Config)  # Use the imported Config class directly
    
    db.init_app(app)
    migrate.init_app(app, db)
    
    from .routes import auth, booking, admin  # Relative import
    app.register_blueprint(auth.bp)
    app.register_blueprint(booking.bp)
    app.register_blueprint(admin.bp)
    
    return app