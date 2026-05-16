import sqlite3
from werkzeug.security import generate_password_hash

def create_sample_data():
    conn = sqlite3.connect('medical.db')
    c = conn.cursor()
    
    print("Creating sample data...")
    
    # Create sample patient
    try:
        c.execute('''INSERT INTO users (name, email, password, role, phone, age, gender, address)
                     VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
                 ('John Doe', 'patient@test.com', generate_password_hash('password123'), 
                  'patient', '9876543210', 30, 'Male', '123 Main St, City'))
        patient_user_id = c.lastrowid
        
        c.execute('INSERT INTO patients (user_id, blood_group) VALUES (?, ?)',
                 (patient_user_id, 'O+'))
        
        print("✓ Sample patient created")
    except sqlite3.IntegrityError:
        print("! Patient already exists")
    
    # Create sample doctors
    doctors_data = [
        ('Dr. Sarah Johnson', 'doctor1@test.com', '9876543211', 'General Physician', 'MBBS, MD', 10, 500),
        ('Dr. Michael Chen', 'doctor2@test.com', '9876543212', 'Cardiologist', 'MBBS, DM', 15, 800),
        ('Dr. Emily Brown', 'doctor3@test.com', '9876543213', 'Dermatologist', 'MBBS, MD', 8, 600),
    ]
    
    for name, email, phone, spec, qual, exp, fee in doctors_data:
        try:
            c.execute('''INSERT INTO users (name, email, password, role, phone)
                         VALUES (?, ?, ?, ?, ?)''',
                     (name, email, generate_password_hash('password123'), 'doctor', phone))
            doctor_user_id = c.lastrowid
            
            c.execute('''INSERT INTO doctors (user_id, specialization, qualification, experience, consultation_fee)
                         VALUES (?, ?, ?, ?, ?)''',
                     (doctor_user_id, spec, qual, exp, fee))
            
            print(f"✓ {name} created")
        except sqlite3.IntegrityError:
            print(f"! {name} already exists")
    
    conn.commit()
    conn.close()
    
    print("\n" + "="*50)
    print("Sample data created successfully!")
    print("="*50)
    print("\nTest Credentials:")
    print("\nPatient Account:")
    print("  Email: patient@test.com")
    print("  Password: password123")
    print("\nDoctor Account:")
    print("  Email: doctor1@test.com")
    print("  Password: password123")
    print("\n" + "="*50)

if __name__ == '__main__':
    create_sample_data()
