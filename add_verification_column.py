"""
Migration script to add verification_id and verification_status columns to doctors table
"""
import sqlite3

def add_verification_columns():
    conn = sqlite3.connect('medical.db')
    cursor = conn.cursor()
    
    try:
        # Check if columns already exist
        cursor.execute("PRAGMA table_info(doctors)")
        columns = [column[1] for column in cursor.fetchall()]
        
        # Add verification_id column if it doesn't exist (without UNIQUE constraint initially)
        if 'verification_id' not in columns:
            cursor.execute('''
                ALTER TABLE doctors 
                ADD COLUMN verification_id TEXT
            ''')
            print("✅ Added verification_id column to doctors table")
        else:
            print("ℹ️  verification_id column already exists")
        
        # Add verification_status column if it doesn't exist
        if 'verification_status' not in columns:
            cursor.execute('''
                ALTER TABLE doctors 
                ADD COLUMN verification_status TEXT DEFAULT 'Pending'
            ''')
            print("✅ Added verification_status column to doctors table")
        else:
            print("ℹ️  verification_status column already exists")
        
        conn.commit()
        print("\n✅ Database migration completed successfully!")
        print("\nNote: verification_id uniqueness is enforced at the application level.")
        
    except sqlite3.Error as e:
        print(f"❌ Error during migration: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == '__main__':
    print("Starting database migration...")
    print("=" * 50)
    add_verification_columns()
    print("=" * 50)
