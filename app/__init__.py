from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
import os
from dotenv import load_dotenv

load_dotenv()

db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()

def create_app():
    app = Flask(__name__, template_folder='../templates', static_folder='../static')
    
    # Configuration
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'default_secret_key')
    
    # Database Configuration
    raw_db_url = os.getenv('DATABASE_URL')
    if raw_db_url and raw_db_url.startswith("postgres://"):
        app.config['SQLALCHEMY_DATABASE_URI'] = raw_db_url.replace("postgres://", "postgresql://", 1)
    else:
        app.config['SQLALCHEMY_DATABASE_URI'] = raw_db_url or 'sqlite:///database.db'
        
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize Extensions
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)

    login_manager.login_view = 'main.student_login' 

    with app.app_context():
        from . import models  # Import models to register them
        from . import routes  # Import routes to register blueprints
        
        # Create tables if they don't exist (useful for local dev with SQLite)
        db.create_all()

        # Create default admin user if not exists
        if not models.User.query.filter_by(username='arun').first():
            db.session.add(models.User(username='arun', password='arun123'))
            db.session.commit()

        app.register_blueprint(routes.bp)

    return app
