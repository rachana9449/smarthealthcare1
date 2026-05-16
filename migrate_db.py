"""
Database Migration Script
Adds consultation_type, prescription, and lab_tests columns to appointments table
"""

import sqlite3

def migrate_database():
    conn = sqlite3.connect('medical.db')
    cursor = conn.cursor()
    
    print("Starting database migration...")
    
    try:
        # Check if columns already exist
        cursor.execute("PRAGMA table_info(appointments)")
        columns = [column[1] for column in cursor.fetchall()]
        
        # Add consultation_type column if it doesn't exist
        if 'consultation_type' not in columns:
            print("Adding consultation_type column...")
            cursor.execute("ALTER TABLE appointments ADD COLUMN consultation_type TEXT DEFAULT 'offline'")
            print("✓ consultation_type column added")
        else:
            print("✓ consultation_type column already exists")
        
        # Add prescription column if it doesn't exist
        if 'prescription' not in columns:
            print("Adding prescription column...")
            cursor.execute("ALTER TABLE appointments ADD COLUMN prescription TEXT")
            print("✓ prescription column added")
        else:
            print("✓ prescription column already exists")
        
        # Add lab_tests column if it doesn't exist
        if 'lab_tests' not in columns:
            print("Adding lab_tests column...")
            cursor.execute("ALTER TABLE appointments ADD COLUMN lab_tests TEXT")
            print("✓ lab_tests column added")
        else:
            print("✓ lab_tests column already exists")
        
        conn.commit()
        print("\n✅ Database migration completed successfully!")
        
    except Exception as e:
        print(f"\n❌ Migration failed: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == '__main__':
    migrate_database()
