"""
Restore original template files
"""

import os

def restore_templates():
    print("Restoring original templates...")
    
    # Delete the new prescription template
    if os.path.exists('templates/add_prescription.html'):
        os.remove('templates/add_prescription.html')
        print("✓ Removed add_prescription.html")
    
    print("\n✅ Templates restored!")
    print("\nNote: book_appointment.html, patient_appointments.html, and doctor_appointments.html")
    print("have been modified. You'll need to manually restore them from a backup if you have one.")
    print("\nOr I can recreate the original versions for you.")

if __name__ == '__main__':
    restore_templates()
