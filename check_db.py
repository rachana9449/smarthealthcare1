import sqlite3
import os

print(f"Current directory: {os.getcwd()}")
print(f"Database file exists: {os.path.exists('medical.db')}")
print(f"Database absolute path: {os.path.abspath('medical.db')}")

conn = sqlite3.connect('medical.db')
cursor = conn.cursor()

cursor.execute("PRAGMA table_info(appointments)")
columns = cursor.fetchall()

print("\nAppointments table columns:")
for col in columns:
    print(f"  {col[1]} ({col[2]})")

conn.close()
