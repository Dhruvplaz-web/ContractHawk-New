from app import db
from datetime import datetime

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    
    full_name = db.Column(db.String(150), nullable=True)
    country = db.Column(db.String(50), default='IN')
    
    # --- MY ADDED AI SETTINGS ---
    negotiation_style = db.Column(db.String(50), default='standard')
    jargon_filter = db.Column(db.String(50), default='professional')
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    documents = db.relationship('Document', backref='owner', lazy=True, cascade="all, delete-orphan")

class Document(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    filename = db.Column(db.String(255), nullable=False)
    risk_score = db.Column(db.Integer, default=0)
    status = db.Column(db.String(50), default='uploaded')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
