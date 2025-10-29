from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

db = SQLAlchemy()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(50), nullable=False)  # 'patient' or 'doctor'
    name = db.Column(db.String(100), nullable=False)
    specialty = db.Column(db.String(100))  # Only for doctors
    bio = db.Column(db.Text)  # Optional bio

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date = db.Column(db.String(50), nullable=False)  # Simple string for date (e.g., '2023-10-01')
    time = db.Column(db.String(50), nullable=False)  # Simple string for time (e.g., '10:00 AM')
    status = db.Column(db.String(50), default='pending')  # 'pending', 'accepted', 'rejected'
    notes = db.Column(db.Text)  # Medical notes by doctor

    patient = db.relationship('User', foreign_keys=[patient_id])
    doctor = db.relationship('User', foreign_keys=[doctor_id])