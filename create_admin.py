import sqlite3
from werkzeug.security import generate_password_hash

def create_admin():
    conn = sqlite3.connect('medical.db')
    c = conn.cursor()
    
    print("Creating admin account...")
    
    try:
        c.execute('''INSERT INTO users (name, email, password, role, phone)
                     VALUES (?, ?, ?, ?, ?)''',
                 ('Admin User', 'admin@test.com', generate_password_hash('admin123'), 
                  'admin', '1234567890'))
        
        conn.commit()
        print("✅ Admin account created successfully!")
        print("\n" + "="*50)
        print("Admin Credentials:")
        print("  Email: admin@test.com")
        print("  Password: admin123")
        print("="*50)
    except sqlite3.IntegrityError:
        print("⚠️  Admin account already exists!")
        print("\n" + "="*50)
        print("Admin Credentials:")
        print("  Email: admin@test.com")
        print("  Password: admin123")
        print("="*50)
    
    conn.close()

if __name__ == '__main__':
    create_admin()
