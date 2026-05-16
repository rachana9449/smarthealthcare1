"""
Restore original database structure by removing new columns
"""

import sqlite3
import os

def restore_database():
    print("Restoring original database structure...")
    
    # Backup current database
    if os.path.exists('medical.db'):
        import shutil
        shutil.copy2('medical.db', 'medical.db.backup')
        print("✓ Created backup: medical.db.backup")
    
    conn = sqlite3.connect('medical.db')
    cursor = conn.cursor()
    
    try:
        # SQLite doesn't support DROP COLUMN directly, so we need to recreate the table
        print("\nRecreating appointments table with original structure...")
        
        # Create new table with original structure
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS appointments_new (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                patient_id INTEGER,
                doctor_id INTEGER,
                appointment_date DATE,
                appointment_time TIME,
                status TEXT DEFAULT 'scheduled',
                reason TEXT,
                notes TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (patient_id) REFERENCES patients(id),
                FOREIGN KEY (doctor_id) REFERENCES doctors(id)
            )
        ''')
        
        # Copy data from old table to new table
        cursor.execute('''
            INSERT INTO appointments_new 
            (id, patient_id, doctor_id, appointment_date, appointment_time, status, reason, notes, created_at)
            SELECT id, patient_id, doctor_id, appointment_date, appointment_time, status, reason, notes, created_at
            FROM appointments
        ''')
        
        # Drop old table
        cursor.execute('DROP TABLE appointments')
        
        # Rename new table
        cursor.execute('ALTER TABLE appointments_new RENAME TO appointments')
        
        conn.commit()
        print("✓ Appointments table restored to original structure")
        print("\n✅ Database restoration completed successfully!")
        print("\nRemoved columns:")
        print("  - consultation_type")
        print("  - prescription")
        print("  - lab_tests")
        print("  - mode")
        print("  - symptoms")
        
    except Exception as e:
        print(f"\n❌ Restoration failed: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == '__main__':
    response = input("This will restore the original database structure. Continue? (yes/no): ")
    if response.lower() == 'yes':
        restore_database()
    else:
        print("Restoration cancelled.")
