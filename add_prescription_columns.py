"""
Migration script to add prescription and lab_tests columns to appointments table
"""
import sqlite3

def add_prescription_columns():
    conn = sqlite3.connect('medical.db')
    cursor = conn.cursor()
    
    try:
        # Check if columns already exist
        cursor.execute("PRAGMA table_info(appointments)")
        columns = [column[1] for column in cursor.fetchall()]
        
        # Add prescription column if it doesn't exist
        if 'prescription' not in columns:
            cursor.execute('''
                ALTER TABLE appointments 
                ADD COLUMN prescription TEXT
            ''')
            print("✅ Added prescription column to appointments table")
        else:
            print("ℹ️  prescription column already exists")
        
        # Add lab_tests column if it doesn't exist
        if 'lab_tests' not in columns:
            cursor.execute('''
                ALTER TABLE appointments 
                ADD COLUMN lab_tests TEXT
            ''')
            print("✅ Added lab_tests column to appointments table")
        else:
            print("ℹ️  lab_tests column already exists")
        
        conn.commit()
        print("\n✅ Database migration completed successfully!")
        print("\nYou can now add prescriptions to appointments.")
        
    except sqlite3.Error as e:
        print(f"❌ Error during migration: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == '__main__':
    print("Starting database migration...")
    print("=" * 50)
    add_prescription_columns()
    print("=" * 50)
