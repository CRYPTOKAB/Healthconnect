from flask import Flask, render_template, redirect, url_for, request, flash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from models import db, User, Appointment
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        name = request.form['name']
        role = request.form['role']
        specialty = request.form.get('specialty') if role == 'doctor' else None
        bio = request.form.get('bio') if role == 'doctor' else None

        if User.query.filter_by(email=email).first():
            flash('Email already registered.')
            return redirect(url_for('register'))

        user = User(email=email, name=name, role=role, specialty=specialty, bio=bio)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        flash('Registration successful! Please log in.')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('dashboard'))
        flash('Invalid credentials.')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
    if current_user.role == 'patient':
        appointments = Appointment.query.filter_by(patient_id=current_user.id).all()
        return render_template('dashboard_patient.html', appointments=appointments)
    elif current_user.role == 'doctor':
        appointments = Appointment.query.filter_by(doctor_id=current_user.id).all()
        return render_template('dashboard_doctor.html', appointments=appointments)

@app.route('/doctors')
@login_required
def doctors():
    doctors = User.query.filter_by(role='doctor').all()
    return render_template('doctors.html', doctors=doctors)

@app.route('/doctor/<int:doctor_id>')
@login_required
def doctor_profile(doctor_id):
    doctor = User.query.get_or_404(doctor_id)
    return render_template('doctor_profile.html', doctor=doctor)

@app.route('/book_appointment/<int:doctor_id>', methods=['GET', 'POST'])
@login_required
def book_appointment(doctor_id):
    if current_user.role != 'patient':
        flash('Only patients can book appointments.')
        return redirect(url_for('dashboard'))
    if request.method == 'POST':
        date = request.form['date']
        time = request.form['time']
        appointment = Appointment(patient_id=current_user.id, doctor_id=doctor_id, date=date, time=time)
        db.session.add(appointment)
        db.session.commit()
        flash('Appointment booked!')
        return redirect(url_for('dashboard'))
    return render_template('book_appointment.html', doctor_id=doctor_id)

@app.route('/appointments')
@login_required
def appointments():
    if current_user.role == 'patient':
        apps = Appointment.query.filter_by(patient_id=current_user.id).all()
    else:
        apps = Appointment.query.filter_by(doctor_id=current_user.id).all()
    return render_template('appointments.html', appointments=apps)

@app.route('/accept_appointment/<int:app_id>')
@login_required
def accept_appointment(app_id):
    if current_user.role != 'doctor':
        flash('Unauthorized.')
        return redirect(url_for('dashboard'))
    appointment = Appointment.query.get_or_404(app_id)
    if appointment.doctor_id != current_user.id:
        flash('Unauthorized.')
        return redirect(url_for('dashboard'))
    appointment.status = 'accepted'
    db.session.commit()
    flash('Appointment accepted.')
    return redirect(url_for('dashboard'))

@app.route('/reject_appointment/<int:app_id>')
@login_required
def reject_appointment(app_id):
    if current_user.role != 'doctor':
        flash('Unauthorized.')
        return redirect(url_for('dashboard'))
    appointment = Appointment.query.get_or_404(app_id)
    if appointment.doctor_id != current_user.id:
        flash('Unauthorized.')
        return redirect(url_for('dashboard'))
    appointment.status = 'rejected'
    db.session.commit()
    flash('Appointment rejected.')
    return redirect(url_for('dashboard'))

@app.route('/record_note/<int:app_id>', methods=['GET', 'POST'])
@login_required
def record_note(app_id):
    if current_user.role != 'doctor':
        flash('Unauthorized.')
        return redirect(url_for('dashboard'))
    appointment = Appointment.query.get_or_404(app_id)
    if appointment.doctor_id != current_user.id:
        flash('Unauthorized.')
        return redirect(url_for('dashboard'))
    if request.method == 'POST':
        notes = request.form['notes']
        appointment.notes = notes
        db.session.commit()
        flash('Notes recorded.')
        return redirect(url_for('dashboard'))
    return render_template('record_note.html', appointment=appointment)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)