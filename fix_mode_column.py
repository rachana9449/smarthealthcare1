"""
Fix mode column - copy data from mode to consultation_type
"""

import sqlite3

def fix_mode_column():
    conn = sqlite3.connect('medical.db')
    cursor = conn.cursor()
    
    print("Fixing mode column...")
    
    try:
        # Copy data from mode to consultation_type where consultation_type is NULL
        cursor.execute("""
            UPDATE appointments 
            SET consultation_type = mode 
            WHERE mode IS NOT NULL 
            AND (consultation_type IS NULL OR consultation_type = '')
        """)
        
        rows_updated = cursor.rowcount
        conn.commit()
        print(f"✓ Updated {rows_updated} rows")
        
        # Set default value for any remaining NULL consultation_type
        cursor.execute("""
            UPDATE appointments 
            SET consultation_type = 'offline' 
            WHERE consultation_type IS NULL OR consultation_type = ''
        """)
        
        rows_updated = cursor.rowcount
        conn.commit()
        print(f"✓ Set default 'offline' for {rows_updated} rows")
        
        print("\n✅ Mode column fix completed successfully!")
        
    except Exception as e:
        print(f"\n❌ Fix failed: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == '__main__':
    fix_mode_column()
