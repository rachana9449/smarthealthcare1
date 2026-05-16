"""
Comprehensive System Test
"""
import sqlite3

def test_database():
    print("=" * 60)
    print("DATABASE STRUCTURE TEST")
    print("=" * 60)
    
    conn = sqlite3.connect('medical.db')
    cursor = conn.cursor()
    
    # Get all tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cursor.fetchall()
    
    print(f"\n✅ Total Tables: {len(tables)}")
    for table in tables:
        print(f"   - {table[0]}")
    
    # Check key columns
    print("\n" + "=" * 60)
    print("KEY COLUMNS CHECK")
    print("=" * 60)
    
    # Check doctors table
    cursor.execute("PRAGMA table_info(doctors)")
    doctor_cols = [col[1] for col in cursor.fetchall()]
    print(f"\n✅ Doctors table columns: {len(doctor_cols)}")
    if 'verification_id' in doctor_cols:
        print("   ✅ verification_id - Present")
    else:
        print("   ❌ verification_id - Missing")
    if 'verification_status' in doctor_cols:
        print("   ✅ verification_status - Present")
    else:
        print("   ❌ verification_status - Missing")
    
    # Check appointments table
    cursor.execute("PRAGMA table_info(appointments)")
    appt_cols = [col[1] for col in cursor.fetchall()]
    print(f"\n✅ Appointments table columns: {len(appt_cols)}")
    if 'prescription' in appt_cols:
        print("   ✅ prescription - Present")
    else:
        print("   ❌ prescription - Missing")
    if 'lab_tests' in appt_cols:
        print("   ✅ lab_tests - Present")
    else:
        print("   ❌ lab_tests - Missing")
    
    # Check data counts
    print("\n" + "=" * 60)
    print("DATA COUNTS")
    print("=" * 60)
    
    cursor.execute("SELECT COUNT(*) FROM users")
    print(f"\n✅ Total Users: {cursor.fetchone()[0]}")
    
    cursor.execute("SELECT COUNT(*) FROM users WHERE role='admin'")
    print(f"   - Admins: {cursor.fetchone()[0]}")
    
    cursor.execute("SELECT COUNT(*) FROM users WHERE role='doctor'")
    print(f"   - Doctors: {cursor.fetchone()[0]}")
    
    cursor.execute("SELECT COUNT(*) FROM users WHERE role='patient'")
    print(f"   - Patients: {cursor.fetchone()[0]}")
    
    cursor.execute("SELECT COUNT(*) FROM appointments")
    print(f"\n✅ Total Appointments: {cursor.fetchone()[0]}")
    
    cursor.execute("SELECT COUNT(*) FROM consultations")
    print(f"✅ Total Consultations: {cursor.fetchone()[0]}")
    
    cursor.execute("SELECT COUNT(*) FROM notifications")
    print(f"✅ Total Notifications: {cursor.fetchone()[0]}")
    
    conn.close()
    
    print("\n" + "=" * 60)
    print("DATABASE TEST COMPLETE")
    print("=" * 60)

if __name__ == '__main__':
    test_database()
