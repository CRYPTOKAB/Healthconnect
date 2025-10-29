from app import app, db
from models import User, Appointment

with app.app_context():
    db.create_all()

    # Sample patients
    patient1 = User(email='user1@example.com', name='John Doe', role='patient')
    patient1.set_password('pass123')
    db.session.add(patient1)

    # Sample doctors
    doctor1 = User(email='doc1@example.com', name='Dr. Alice Smith', role='doctor', specialty='Cardiology', bio='Experienced cardiologist.')
    doctor1.set_password('pass123')
    db.session.add(doctor1)

    doctor2 = User(email='doc2@example.com', name='Dr. Bob Johnson', role='doctor', specialty='Dermatology', bio='Skin care expert.')
    doctor2.set_password('pass123')
    db.session.add(doctor2)

    db.session.commit()
    print("Database seeded with sample data.")