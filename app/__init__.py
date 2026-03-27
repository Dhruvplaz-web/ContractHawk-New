import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

load_dotenv()
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY', 'dev_fallback_key')
    
    basedir = os.path.abspath(os.path.dirname(__file__))
    db_path = os.path.join(basedir, 'contracthawk.db')
    
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}?timeout=20'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db.init_app(app)
    
    with app.app_context():
        from app import models
        db.create_all()
        
        # Register ALL THREE Blueprints now
        from app.routes.page_routes import page_bp
        from app.routes.auth_routes import auth_bp
        from app.routes.api_routes import api_bp
        
        app.register_blueprint(page_bp)
        app.register_blueprint(auth_bp)
        app.register_blueprint(api_bp)

    return app
