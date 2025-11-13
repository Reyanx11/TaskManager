from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime
from itsdangerous import URLSafeTimedSerializer
from flask import current_app
from werkzeug.utils import secure_filename
import os 

db = SQLAlchemy()

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    confirmed = db.Column(db.Boolean, default=False)
    tasks = db.relationship('Task', backref='owner', lazy=True)
    otp = db.Column(db.String(6), nullable=True)
    otp_created_at = db.Column(db.DateTime, nullable=True)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=True)  # ✅ Added
    due_date = db.Column(db.DateTime, nullable=True)  # ✅ Added
    priority = db.Column(db.String(20), default='Medium')  # ✅ Added
    completed = db.Column(db.Boolean, default=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    @property
    def time_remaining(self):
        if self.due_date:
            delta = self.due_date - datetime.utcnow()
            if delta.total_seconds() > 0:
                days = delta.days
                hours = delta.seconds // 3600
                minutes = (delta.seconds % 3600) // 60
                return f"{days}d {hours}h {minutes}m"
            else:
                return "Expired"
        return "No due date"

# ✅ Use current_app safely within Flask context
def generate_confirmation_token(email):
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    return serializer.dumps(email, salt='email-confirm-salt')

def confirm_token(token, expiration=3600):
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    try:
        email = serializer.loads(token, salt='email-confirm-salt', max_age=expiration)
    except:
        return False
    return email

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)          # Slightly longer title
    content = db.Column(db.Text, nullable=True)
    filename = db.Column(db.String(200), nullable=True)        # Store uploaded PDF filename
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow) 