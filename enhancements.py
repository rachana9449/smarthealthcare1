"""
ENHANCEMENTS MODULE
Adds new features to existing Flask healthcare app WITHOUT breaking current functionality
"""

from flask import Blueprint, render_template, request, redirect, url_for, session, flash, jsonify
from functools import wraps
import sqlite3
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Create Blueprint for new features
enhancements_bp = Blueprint('enhancements', __name__)

# Database helper
def get_db_connection():
    conn = sqlite3.connect('medical.db')
    conn.row_factory = sqlite3.Row
    return conn

# ==================== DISEASE-TO-SPECIALIZATION MAPPING ====================
DISEASE_SPECIALIZATION_MAP = {
    'Fungal infection': 'Dermatologist',
    'Allergy': 'Allergist',
    'GERD': 'Gastroenterologist',
    'Chronic cholestasis': 'Hepatologist',
    'Drug Reaction': 'Allergist',
    'Peptic ulcer diseae': 'Gastroenterologist',
    'AIDS': 'Infectious Disease Specialist',
    'Diabetes': 'Endocrinologist',
    'Gastroenteritis': 'Gastroenterologist',
    'Bronchial Asthma': 'Pulmonologist',
    'Hypertension': 'Cardiologist',
    'Migraine': 'Neurologist',
    'Cervical spondylosis': 'Orthopedist',
    'Paralysis (brain hemorrhage)': 'Neurologist',
    'Jaundice': 'Hepatologist',
    'Malaria': 'Infectious Disease Specialist',
    'Chicken pox': 'Infectious Disease Specialist',
    'Dengue': 'Infectious Disease Specialist',
    'Typhoid': 'Infectious Disease Specialist',
    'hepatitis A': 'Hepatologist',
    'Hepatitis B': 'Hepatologist',
    'Hepatitis C': 'Hepatologist',
    'Hepatitis D': 'Hepatologist',
    'Hepatitis E': 'Hepatologist',
    'Alcoholic hepatitis': 'Hepatologist',
    'Tuberculosis': 'Pulmonologist',
    'Common Cold': 'General Physician',
    'Pneumonia': 'Pulmonologist',
    'Dimorphic hemmorhoids(piles)': 'Proctologist',
    'Heart attack': 'Cardiologist',
    'Varicose veins': 'Vascular Surgeon',
    'Hypothyroidism': 'Endocrinologist',
    'Hyperthyroidism': 'Endocrinologist',
    'Hypoglycemia': 'Endocrinologist',
    'Osteoarthristis': 'Orthopedist',
    'Arthritis': 'Rheumatologist',
    '(vertigo) Paroymsal  Positional Vertigo': 'ENT Specialist',
    'Acne': 'Dermatologist',
    'Urinary tract infection': 'Urologist',
    'Psoriasis': 'Dermatologist',
    'Impetigo': 'Dermatologist'
}

def get_specialization_for_disease(disease):
    """Get recommended specialization for a disease"""
    return DISEASE_SPECIALIZATION_MAP.get(disease, 'General Physician')

# ==================== DOCTOR RECOMMENDATION ====================
@enhancements_bp.route('/api/recommend-doctors', methods=['POST'])
def recommend_doctors():
    """
    Recommend doctors based on predicted disease
    Called from prediction results page
    """
    try:
        data = request.get_json()
        disease = data.get('disease')
        
        if not disease:
            return jsonify({'error': 'Disease not provided'}), 400
        
        # Get specialization for disease
        specialization = get_specialization_for_disease(disease)
        
        # Find doctors with matching specialization
        conn = get_db_connection()
        doctors = conn.execute('''
            SELECT u.id, u.name, u.email, u.phone,
                   d.specialization, d.qualification, d.experience, d.consultation_fee,
                   COALESCE(AVG(f.rating), 0) as avg_rating,
                   COUNT(f.id) as review_count
            FROM users u
            JOIN doctors d ON u.id = d.user_id
            LEFT JOIN feedback f ON u.id = f.doctor_id
            WHERE u.role = 'doctor' AND d.available = 1
            AND (d.specialization LIKE ? OR d.specialization = 'General Physician')
            GROUP BY u.id
            ORDER BY avg_rating DESC, d.consultation_fee ASC
            LIMIT 10
        ''', (f'%{specialization}%',)).fetchall()
        conn.close()
        
        # Format results
        recommended_doctors = []
        for doc in doctors:
            recommended_doctors.append({
                'id': doc['id'],
                'name': doc['name'],
                'specialization': doc['specialization'],
                'qualification': doc['qualification'],
                'experience': doc['experience'],
                'fee': doc['consultation_fee'],
                'rating': round(doc['avg_rating'], 1),
                'reviews': doc['review_count'],
                'phone': doc['phone']
            })
        
        return jsonify({
            'disease': disease,
            'recommended_specialization': specialization,
            'doctors': recommended_doctors
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ==================== ENHANCED APPOINTMENT BOOKING ====================
@enhancements_bp.route('/api/book-appointment-enhanced', methods=['POST'])
def book_appointment_enhanced():
    """
    Enhanced appointment booking with notifications
    """
    try:
        if 'user_id' not in session or session.get('role') != 'patient':
            return jsonify({'error': 'Unauthorized'}), 401
        
        data = request.get_json()
        doctor_id = data.get('doctor_id')
        appointment_date = data.get('date')
        appointment_time = data.get('time')
        consultation_mode = data.get('mode', 'online')  # online or offline
        symptoms = data.get('symptoms', '')
        
        # Validate inputs
        if not all([doctor_id, appointment_date, appointment_time]):
            return jsonify({'error': 'Missing required fields'}), 400
        
        # Create appointment
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO appointments 
            (patient_id, doctor_id, appointment_date, appointment_time, status, consultation_type, reason)
            VALUES (?, ?, ?, ?, 'pending', ?, ?)
        ''', (session['user_id'], doctor_id, appointment_date, appointment_time, consultation_mode, symptoms))
        
        appointment_id = cursor.lastrowid
        
        # Get patient and doctor details
        patient = conn.execute('SELECT name, email, phone FROM users WHERE id = ?', 
                              (session['user_id'],)).fetchone()
        doctor = conn.execute('SELECT name, email, phone FROM users WHERE id = ?', 
                             (doctor_id,)).fetchone()
        
        # Create notification for doctor
        cursor.execute('''
            INSERT INTO notifications (user_id, title, message, type, related_id)
            VALUES (?, ?, ?, 'appointment', ?)
        ''', (
            doctor_id,
            'New Appointment Request',
            f'New {consultation_mode} appointment from {patient["name"]} on {appointment_date} at {appointment_time}',
            appointment_id
        ))
        
        conn.commit()
        conn.close()
        
        # Send email notification to doctor
        send_appointment_email(
            doctor['email'],
            doctor['name'],
            patient['name'],
            appointment_date,
            appointment_time,
            consultation_mode
        )
        
        # Send SMS notification (mock or real)
        send_appointment_sms(
            doctor['phone'],
            patient['name'],
            appointment_date,
            appointment_time
        )
        
        return jsonify({
            'success': True,
            'appointment_id': appointment_id,
            'message': 'Appointment booked successfully. Doctor has been notified.'
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ==================== NOTIFICATION SYSTEM ====================
def send_appointment_email(to_email, doctor_name, patient_name, date, time, mode):
    """Send email notification to doctor"""
    try:
        # Gmail SMTP configuration
        smtp_server = "smtp.gmail.com"
        smtp_port = 587
        sender_email = "your-email@gmail.com"  # Configure this
        sender_password = "your-app-password"  # Use App Password, not regular password
        
        # Create message
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = to_email
        msg['Subject'] = f'New Appointment Request - {date}'
        
        body = f"""
        Dear Dr. {doctor_name},
        
        You have a new appointment request:
        
        Patient: {patient_name}
        Date: {date}
        Time: {time}
        Mode: {mode.capitalize()} Consultation
        
        Please log in to your dashboard to accept or reject this appointment.
        
        Best regards,
        MediConnect Team
        """
        
        msg.attach(MIMEText(body, 'plain'))
        
        # Send email
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, sender_password)
        server.send_message(msg)
        server.quit()
        
        print(f"Email sent to {to_email}")
        return True
    
    except Exception as e:
        print(f"Email error: {e}")
        return False

def send_appointment_sms(phone, patient_name, date, time):
    """Send SMS notification (mock implementation)"""
    try:
        # Mock SMS - In production, use Twilio API
        sms_message = f"New appointment from {patient_name} on {date} at {time}. Check your dashboard."
        print(f"SMS to {phone}: {sms_message}")
        
        # Real Twilio implementation (uncomment and configure):
        """
        from twilio.rest import Client
        account_sid = 'your_account_sid'
        auth_token = 'your_auth_token'
        client = Client(account_sid, auth_token)
        
        message = client.messages.create(
            body=sms_message,
            from_='+1234567890',  # Your Twilio number
            to=phone
        )
        """
        
        return True
    
    except Exception as e:
        print(f"SMS error: {e}")
        return False

# ==================== DOCTOR ACTIONS ====================
@enhancements_bp.route('/api/appointment/action', methods=['POST'])
def appointment_action():
    """Doctor accepts or rejects appointment"""
    try:
        if 'user_id' not in session or session.get('role') != 'doctor':
            return jsonify({'error': 'Unauthorized'}), 401

        data           = request.get_json()
        appointment_id = data.get('appointment_id')
        action         = data.get('action')  # 'accept' or 'reject'

        if action not in ['accept', 'reject']:
            return jsonify({'error': 'Invalid action'}), 400

        conn   = get_db_connection()
        cursor = conn.cursor()

        # Get the doctor's doctors.id from their user_id
        doctor = conn.execute(
            'SELECT id, user_id FROM doctors WHERE user_id = ?', (session['user_id'],)
        ).fetchone()

        if not doctor:
            conn.close()
            return jsonify({'error': 'Doctor profile not found'}), 400
        
        # Get doctor name
        doctor_user = conn.execute(
            'SELECT name FROM users WHERE id = ?', (doctor['user_id'],)
        ).fetchone()

        new_status = 'confirmed' if action == 'accept' else 'cancelled'

        cursor.execute(
            'UPDATE appointments SET status = ? WHERE id = ? AND doctor_id = ?',
            (new_status, appointment_id, doctor['id'])
        )

        # Get appointment + patient user details
        appointment = conn.execute('''
            SELECT a.*,
                   u.name  as patient_name,
                   u.email as patient_email,
                   u.id    as patient_user_id
            FROM appointments a
            JOIN patients p ON a.patient_id = p.id
            JOIN users u    ON p.user_id = u.id
            WHERE a.id = ?
        ''', (appointment_id,)).fetchone()

        if appointment:
            # Create in-app notification
            cursor.execute('''
                INSERT INTO notifications (user_id, title, message, type)
                VALUES (?, ?, ?, ?)
            ''', (
                appointment['patient_user_id'],
                f'Appointment {"Confirmed" if action == "accept" else "Rejected"}',
                f'Your appointment on {appointment["appointment_date"]} at {appointment["appointment_time"]} has been {"confirmed" if action == "accept" else "rejected"} by the doctor.',
                'appointment'
            ))
            
            # Send email notification when doctor accepts
            if action == 'accept':
                try:
                    from email_notifications import send_appointment_accepted_email
                    mode = appointment['mode'] if appointment['mode'] else 'in-person'
                    
                    # Log to file for debugging
                    with open('email_debug.log', 'a') as f:
                        f.write(f"\n[{datetime.now()}] Sending acceptance email\n")
                        f.write(f"  To: {appointment['patient_email']}\n")
                        f.write(f"  Patient: {appointment['patient_name']}\n")
                        f.write(f"  Doctor: {doctor_user['name']}\n")
                    
                    print(f"[Enhancement API] Sending acceptance email to {appointment['patient_email']}", flush=True)
                    
                    result = send_appointment_accepted_email(
                        patient_email=appointment['patient_email'],
                        patient_name=appointment['patient_name'],
                        doctor_name=doctor_user['name'],
                        date=appointment['appointment_date'],
                        time=appointment['appointment_time'],
                        mode=mode,
                        appointment_id=appointment_id
                    )
                    
                    with open('email_debug.log', 'a') as f:
                        f.write(f"  Result: {result}\n")
                    
                    print(f"[Enhancement API] Email sent successfully (result: {result})", flush=True)
                except Exception as email_error:
                    with open('email_debug.log', 'a') as f:
                        f.write(f"  ERROR: {email_error}\n")
                    print(f"[Enhancement API] Email failed: {email_error}", flush=True)
                    # Don't fail the whole request if email fails

        conn.commit()
        conn.close()

        return jsonify({'success': True, 'message': f'Appointment {action}ed successfully'})

    except Exception as e:
        print(f"[Enhancement API] Error: {e}")
        return jsonify({'error': str(e)}), 500

# ==================== PRESCRIPTION MANAGEMENT ====================
@enhancements_bp.route('/api/add-prescription', methods=['POST'])
def add_prescription():
    """Doctor adds prescription after consultation"""
    try:
        if 'user_id' not in session or session.get('role') != 'doctor':
            return jsonify({'error': 'Unauthorized'}), 401
        
        data = request.get_json()
        consultation_id = data.get('consultation_id')
        medicines = data.get('medicines', '')  # JSON string or text
        notes = data.get('notes', '')
        suggested_tests = data.get('suggested_tests', '')  # e.g., "CT Scan, MRI"
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Check if prescription table exists, if not create it
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS prescriptions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                consultation_id INTEGER,
                doctor_id INTEGER,
                patient_id INTEGER,
                medicines TEXT,
                notes TEXT,
                suggested_tests TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (consultation_id) REFERENCES consultations(id),
                FOREIGN KEY (doctor_id) REFERENCES users(id),
                FOREIGN KEY (patient_id) REFERENCES users(id)
            )
        ''')
        
        # Get consultation details
        consultation = conn.execute('''
            SELECT patient_id FROM consultations WHERE id = ?
        ''', (consultation_id,)).fetchone()
        
        if not consultation:
            return jsonify({'error': 'Consultation not found'}), 404
        
        # Insert prescription
        cursor.execute('''
            INSERT INTO prescriptions 
            (consultation_id, doctor_id, patient_id, medicines, notes, suggested_tests)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (consultation_id, session['user_id'], consultation['patient_id'], 
              medicines, notes, suggested_tests))
        
        prescription_id = cursor.lastrowid
        
        # Notify patient
        cursor.execute('''
            INSERT INTO notifications (user_id, title, message, type, related_id)
            VALUES (?, ?, ?, 'prescription', ?)
        ''', (
            consultation['patient_id'],
            'Prescription Added',
            'Your doctor has added a prescription. View it in your medical records.',
            prescription_id
        ))
        
        conn.commit()
        conn.close()
        
        return jsonify({
            'success': True,
            'prescription_id': prescription_id,
            'message': 'Prescription added successfully'
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@enhancements_bp.route('/api/get-prescription/<int:consultation_id>')
def get_prescription(consultation_id):
    """Get prescription for a consultation"""
    try:
        if 'user_id' not in session:
            return jsonify({'error': 'Unauthorized'}), 401
        
        conn = get_db_connection()
        prescription = conn.execute('''
            SELECT p.*, d.name as doctor_name, d.specialization
            FROM prescriptions p
            LEFT JOIN doctors doc ON p.doctor_id = doc.user_id
            LEFT JOIN users d ON p.doctor_id = d.id
            WHERE p.consultation_id = ?
        ''', (consultation_id,)).fetchone()
        conn.close()
        
        if not prescription:
            return jsonify({'error': 'Prescription not found'}), 404
        
        return jsonify({
            'id': prescription['id'],
            'medicines': prescription['medicines'],
            'notes': prescription['notes'],
            'suggested_tests': prescription['suggested_tests'],
            'doctor_name': prescription['doctor_name'],
            'created_at': prescription['created_at']
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ==================== EMERGENCY SERVICES ====================
@enhancements_bp.route('/api/emergency/nearby', methods=['POST'])
def emergency_nearby():
    """Find nearby hospitals and ambulance services"""
    try:
        data = request.get_json()
        latitude = data.get('latitude')
        longitude = data.get('longitude')
        
        # Mock data - In production, integrate with Google Maps API
        nearby_services = {
            'hospitals': [
                {
                    'name': 'City General Hospital',
                    'address': '123 Main St',
                    'phone': '108',
                    'distance': '2.5 km',
                    'emergency': True
                },
                {
                    'name': 'Apollo Hospital',
                    'address': '456 Health Ave',
                    'phone': '1800-123-4567',
                    'distance': '3.8 km',
                    'emergency': True
                }
            ],
            'ambulances': [
                {
                    'service': 'Government Ambulance',
                    'phone': '108',
                    'type': 'Free'
                },
                {
                    'service': 'Private Ambulance Service',
                    'phone': '1800-AMBULANCE',
                    'type': 'Paid'
                }
            ]
        }
        
        return jsonify(nearby_services)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ==================== INITIALIZE TABLES ====================
def init_enhancement_tables():
    """Create additional tables if they don't exist"""
    conn = sqlite3.connect('medical.db')
    cursor = conn.cursor()
    
    # Prescriptions table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS prescriptions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            consultation_id INTEGER,
            doctor_id INTEGER,
            patient_id INTEGER,
            medicines TEXT,
            notes TEXT,
            suggested_tests TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (consultation_id) REFERENCES consultations(id),
            FOREIGN KEY (doctor_id) REFERENCES users(id),
            FOREIGN KEY (patient_id) REFERENCES users(id)
        )
    ''')
    
    # Add mode column to appointments if it doesn't exist
    try:
        cursor.execute('ALTER TABLE appointments ADD COLUMN mode TEXT DEFAULT "online"')
    except:
        pass  # Column already exists
    
    # Add symptoms column to appointments if it doesn't exist
    try:
        cursor.execute('ALTER TABLE appointments ADD COLUMN symptoms TEXT')
    except:
        pass  # Column already exists
    
    conn.commit()
    conn.close()
    print("Enhancement tables initialized successfully")
