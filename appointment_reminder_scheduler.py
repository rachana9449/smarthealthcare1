"""
Appointment Reminder Scheduler
Checks for upcoming appointments and sends reminder emails 5 minutes before
"""

import sqlite3
import time
from datetime import datetime, timedelta
import threading
import os
import sys

# Import email functions
try:
    from email_notifications import send_appointment_reminder, EMAIL_ENABLED
    print("[Reminder] Email notification module loaded")
except ImportError as e:
    print(f"[Reminder] Warning: Could not import email_notifications: {e}")
    EMAIL_ENABLED = False
    def send_appointment_reminder(*args, **kwargs):
        return False

# Configuration
CHECK_INTERVAL = 60  # Check every 60 seconds
REMINDER_MINUTES = 5  # Send reminder 5 minutes before appointment

# Get correct database path (same directory as this script)
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_PATH = os.path.join(SCRIPT_DIR, 'medical.db')

# Track which appointments have already been reminded
reminded_appointments = set()

def get_db():
    """Get database connection"""
    if not os.path.exists(DATABASE_PATH):
        print(f"[Reminder] [WARNING] Database not found at: {DATABASE_PATH}")
        return None
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def check_and_send_reminders():
    """Check for upcoming appointments and send reminders"""
    if not EMAIL_ENABLED:
        print("[Reminder] [WARNING] Email not enabled, skipping reminder check")
        return
    
    try:
        conn = get_db()
        if not conn:
            return
        
        # Get current time and time window for reminders
        now = datetime.now()
        reminder_time_start = now + timedelta(minutes=REMINDER_MINUTES)
        reminder_time_end = now + timedelta(minutes=REMINDER_MINUTES + 1)
        
        # Format for SQL comparison
        current_date = now.strftime('%Y-%m-%d')
        current_time = now.strftime('%H:%M:%S')
        reminder_start_str = reminder_time_start.strftime('%H:%M:%S')
        reminder_end_str = reminder_time_end.strftime('%H:%M:%S')
        
        print(f"[Reminder] Checking at {current_time} for appointments between {reminder_start_str} and {reminder_end_str}")
        
        # Find appointments that:
        # 1. Are scheduled or confirmed
        # 2. Are happening today in the next 5-6 minutes
        # 3. Haven't been reminded yet
        query = '''
            SELECT 
                a.id as appointment_id,
                a.appointment_date,
                a.appointment_time,
                a.mode,
                a.status,
                p_user.name as patient_name,
                p_user.email as patient_email,
                d_user.name as doctor_name,
                d_user.email as doctor_email,
                d_user.id as doctor_user_id
            FROM appointments a
            JOIN patients p ON a.patient_id = p.id
            JOIN users p_user ON p.user_id = p_user.id
            JOIN doctors d ON a.doctor_id = d.id
            JOIN users d_user ON d.user_id = d_user.id
            WHERE a.status IN ('scheduled', 'confirmed')
            AND a.appointment_date = ?
            AND a.appointment_time >= ?
            AND a.appointment_time <= ?
        '''
        
        appointments = conn.execute(query, (
            current_date, 
            reminder_start_str, 
            reminder_end_str
        )).fetchall()
        
        print(f"[Reminder] Found {len(appointments)} appointments in reminder window")
        
        # Send reminders
        for appt in appointments:
            appt_id = appt['appointment_id']
            
            # Skip if already reminded
            if appt_id in reminded_appointments:
                print(f"[Reminder] Skipping appointment #{appt_id} (already reminded)")
                continue
            
            mode = appt['mode'] if appt['mode'] else 'in-person'
            
            print(f"[Reminder] Processing appointment #{appt_id}:")
            print(f"  - Patient: {appt['patient_name']} ({appt['patient_email']})")
            print(f"  - Doctor: {appt['doctor_name']} ({appt['doctor_email']})")
            print(f"  - Time: {appt['appointment_date']} {appt['appointment_time']}")
            print(f"  - Mode: {mode}")
            print(f"  - Status: {appt['status']}")
            
            # Send reminder to patient
            print(f"[Reminder] Sending to patient: {appt['patient_name']}")
            patient_sent = send_appointment_reminder(
                email=appt['patient_email'],
                name=appt['patient_name'],
                role='patient',
                doctor_name=appt['doctor_name'],
                patient_name=appt['patient_name'],
                date=appt['appointment_date'],
                time=appt['appointment_time'],
                appointment_id=appt_id,
                mode=mode
            )
            
            # Send reminder to doctor
            print(f"[Reminder] Sending to doctor: {appt['doctor_name']}")
            doctor_sent = send_appointment_reminder(
                email=appt['doctor_email'],
                name=appt['doctor_name'],
                role='doctor',
                doctor_name=appt['doctor_name'],
                patient_name=appt['patient_name'],
                date=appt['appointment_date'],
                time=appt['appointment_time'],
                appointment_id=appt_id,
                mode=mode
            )
            
            # Mark as reminded
            reminded_appointments.add(appt_id)
            
            if patient_sent or doctor_sent:
                print(f"[Reminder] [SUCCESS] Reminders sent for appointment #{appt_id}")
            else:
                print(f"[Reminder] [WARNING] Failed to send reminders for appointment #{appt_id}")
        
        conn.close()
        
    except Exception as e:
        print(f"[Reminder] [ERROR] Error checking reminders: {e}")
        import traceback
        traceback.print_exc()

def cleanup_old_reminders():
    """Remove old appointment IDs from reminded set to prevent memory buildup"""
    try:
        conn = get_db()
        if not conn:
            return
        
        # Get appointments from last 24 hours
        yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
        recent_appointments = conn.execute(
            'SELECT id FROM appointments WHERE appointment_date >= ?',
            (yesterday,)
        ).fetchall()
        
        recent_ids = {row['id'] for row in recent_appointments}
        
        # Remove old IDs from reminded set
        global reminded_appointments
        old_count = len(reminded_appointments)
        reminded_appointments = reminded_appointments.intersection(recent_ids)
        new_count = len(reminded_appointments)
        
        if old_count != new_count:
            print(f"[Reminder] Cleaned up {old_count - new_count} old reminder records")
        
        conn.close()
        
    except Exception as e:
        print(f"[Reminder] Warning: Could not cleanup old reminders: {e}")

def reminder_scheduler_loop():
    """Main scheduler loop - runs continuously in background"""
    print("[Reminder] [INFO] Appointment reminder scheduler started")
    print(f"[Reminder] Database path: {DATABASE_PATH}")
    print(f"[Reminder] Checking every {CHECK_INTERVAL} seconds for appointments in {REMINDER_MINUTES} minutes")
    print(f"[Reminder] Email enabled: {EMAIL_ENABLED}")
    
    if not EMAIL_ENABLED:
        print("[Reminder] [WARNING] Email not configured - reminders will not be sent")
        print("[Reminder] Configure GMAIL_USER and GMAIL_PASSWORD in .env to enable")
        return
    
    cleanup_counter = 0
    
    while True:
        try:
            check_and_send_reminders()
            
            # Cleanup every hour (60 checks at 60 second intervals)
            cleanup_counter += 1
            if cleanup_counter >= 60:
                cleanup_old_reminders()
                cleanup_counter = 0
            
            time.sleep(CHECK_INTERVAL)
            
        except KeyboardInterrupt:
            print("[Reminder] Scheduler stopped by user")
            break
        except Exception as e:
            print(f"[Reminder] [ERROR] Scheduler error: {e}")
            import traceback
            traceback.print_exc()
            time.sleep(CHECK_INTERVAL)

def start_reminder_scheduler():
    """Start the reminder scheduler in a background thread"""
    if not EMAIL_ENABLED:
        print("[Reminder] [WARNING] Reminder scheduler disabled (email not configured)")
        print("[Reminder] Set GMAIL_USER and GMAIL_PASSWORD in .env to enable reminders")
        return None
    
    print("[Reminder] Starting reminder scheduler thread...")
    scheduler_thread = threading.Thread(target=reminder_scheduler_loop, daemon=True)
    scheduler_thread.start()
    print("[Reminder] [SUCCESS] Reminder scheduler thread started")
    return scheduler_thread

if __name__ == '__main__':
    # Run standalone for testing
    print("[Reminder] Running in standalone mode")
    reminder_scheduler_loop()
