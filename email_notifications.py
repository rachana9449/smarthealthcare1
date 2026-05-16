"""
Email Notification System for MediConnect
Sends emails for appointments, video calls, and verifications
"""

import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Email configuration from environment variables
GMAIL_USER = os.environ.get('GMAIL_USER', '').strip()
GMAIL_PASSWORD = os.environ.get('GMAIL_PASSWORD', '').strip()
EMAIL_ENABLED = bool(GMAIL_USER and GMAIL_PASSWORD)

# Base URL for links (change in production)
BASE_URL = os.environ.get('BASE_URL', 'http://localhost:5000')

def send_email(to_email, subject, body_html):
    """
    Send HTML email using Gmail SMTP
    
    Args:
        to_email: Recipient email address
        subject: Email subject
        body_html: HTML content of email
    
    Returns:
        bool: True if sent successfully, False otherwise
    """
    if not EMAIL_ENABLED:
        safe_subject = subject.encode('ascii', 'ignore').decode()
        print(f"[Email] [WARNING] Skipped (not configured): {safe_subject} to {to_email}")
        print(f"[Email] Set GMAIL_USER and GMAIL_PASSWORD in .env to enable emails")
        return False
    
    try:
        msg = MIMEMultipart('alternative')
        msg['From'] = GMAIL_USER
        msg['To'] = to_email
        msg['Subject'] = subject
        
        html_part = MIMEText(body_html, 'html')
        msg.attach(html_part)
        
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(GMAIL_USER, GMAIL_PASSWORD)
            server.send_message(msg)
        
        safe_subject = subject.encode('ascii', 'ignore').decode()
        print(f"[Email] [SUCCESS] Sent: {safe_subject} to {to_email}")
        return True
    except Exception as e:
        print(f"[Email] [ERROR] Failed to send to {to_email}: {str(e)}")
        return False


def send_appointment_confirmation(patient_email, patient_name, doctor_name, 
                                 specialization, date, time, mode, appointment_id):
    """
    Send appointment confirmation email to patient
    
    Args:
        patient_email: Patient's email address
        patient_name: Patient's name
        doctor_name: Doctor's name
        specialization: Doctor's specialization
        date: Appointment date
        time: Appointment time
        mode: Consultation mode (online/in-person)
        appointment_id: Appointment ID for video call link
    """
    
    # Add video call button if online
    video_call_section = ""
    if mode in ['online', 'video']:
        video_call_section = f"""
        <div style="text-align: center; margin: 30px 0;">
            <a href="{BASE_URL}/video-call/{appointment_id}" 
               style="background: linear-gradient(135deg, #28a745 0%, #20c997 100%); 
                      color: white; padding: 15px 40px; text-decoration: none; 
                      border-radius: 8px; display: inline-block; font-weight: bold; 
                      font-size: 16px; box-shadow: 0 4px 15px rgba(40, 167, 69, 0.3);">
                🎥 Join Video Consultation
            </a>
            <p style="color: #666; font-size: 13px; margin-top: 10px;">
                Click this button when it's time for your appointment
            </p>
        </div>
        """
    
    subject = "✅ Appointment Confirmed - MediConnect"
    body = f"""
    <html>
    <head>
        <style>
            body {{ font-family: 'Segoe UI', Arial, sans-serif; line-height: 1.6; color: #333; }}
            .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
            .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                      color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }}
            .content {{ background: #ffffff; padding: 30px; border: 1px solid #e0e0e0; }}
            .details-box {{ background: #f8f9fa; padding: 20px; border-radius: 10px; 
                           margin: 20px 0; border-left: 4px solid #667eea; }}
            .footer {{ background: #f8f9fa; padding: 20px; text-align: center; 
                      border-radius: 0 0 10px 10px; color: #666; font-size: 12px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1 style="margin: 0; font-size: 28px;">🏥 MediConnect</h1>
                <p style="margin: 10px 0 0 0; opacity: 0.9;">Healthcare Management System</p>
            </div>
            
            <div class="content">
                <h2 style="color: #667eea; margin-top: 0;">Appointment Confirmed!</h2>
                
                <p>Dear <strong>{patient_name}</strong>,</p>
                
                <p>Your appointment has been successfully booked. We look forward to serving you!</p>
                
                <div class="details-box">
                    <h3 style="margin-top: 0; color: #333;">📋 Appointment Details:</h3>
                    <table style="width: 100%; border-collapse: collapse;">
                        <tr>
                            <td style="padding: 8px 0;"><strong>Doctor:</strong></td>
                            <td style="padding: 8px 0;">Dr. {doctor_name}</td>
                        </tr>
                        <tr>
                            <td style="padding: 8px 0;"><strong>Specialization:</strong></td>
                            <td style="padding: 8px 0;">{specialization}</td>
                        </tr>
                        <tr>
                            <td style="padding: 8px 0;"><strong>Date:</strong></td>
                            <td style="padding: 8px 0;">{date}</td>
                        </tr>
                        <tr>
                            <td style="padding: 8px 0;"><strong>Time:</strong></td>
                            <td style="padding: 8px 0;">{time}</td>
                        </tr>
                        <tr>
                            <td style="padding: 8px 0;"><strong>Mode:</strong></td>
                            <td style="padding: 8px 0;">{mode.title()}</td>
                        </tr>
                    </table>
                </div>
                
                {video_call_section}
                
                <p style="margin-top: 30px;">
                    <strong>📱 Manage Your Appointment:</strong><br>
                    View, reschedule, or cancel your appointment from your dashboard:<br>
                    <a href="{BASE_URL}/patient/appointments" 
                       style="color: #667eea; text-decoration: none; font-weight: bold;">
                        View My Appointments →
                    </a>
                </p>
                
                <div style="background: #fff3cd; padding: 15px; border-radius: 8px; margin-top: 20px; border-left: 4px solid #ffc107;">
                    <p style="margin: 0; color: #856404;">
                        <strong>⏰ Reminder:</strong> Please arrive/join 5 minutes before your scheduled time.
                    </p>
                </div>
            </div>
            
            <div class="footer">
                <p style="margin: 0;">Thank you for choosing MediConnect!</p>
                <p style="margin: 10px 0 0 0;">
                    This is an automated email. Please do not reply to this message.
                </p>
            </div>
        </div>
    </body>
    </html>
    """
    
    return send_email(patient_email, subject, body)


def send_video_call_reminder(patient_email, patient_name, doctor_name, 
                            date, time, appointment_id):
    """
    Send video call reminder email to patient
    """
    
    subject = "🎥 Video Consultation Reminder - MediConnect"
    body = f"""
    <html>
    <head>
        <style>
            body {{ font-family: 'Segoe UI', Arial, sans-serif; line-height: 1.6; color: #333; }}
            .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
            .header {{ background: linear-gradient(135deg, #28a745 0%, #20c997 100%); 
                      color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }}
            .content {{ background: #ffffff; padding: 30px; border: 1px solid #e0e0e0; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1 style="margin: 0; font-size: 28px;">🎥 Video Consultation</h1>
                <p style="margin: 10px 0 0 0; opacity: 0.9;">Your appointment is ready!</p>
            </div>
            
            <div class="content">
                <h2 style="color: #28a745; margin-top: 0;">Time for Your Consultation!</h2>
                
                <p>Dear <strong>{patient_name}</strong>,</p>
                
                <p>This is a reminder for your video consultation:</p>
                
                <div style="background: #e3f2fd; padding: 20px; border-radius: 10px; margin: 20px 0; border-left: 4px solid #2196f3;">
                    <p style="margin: 5px 0;"><strong>Doctor:</strong> Dr. {doctor_name}</p>
                    <p style="margin: 5px 0;"><strong>Date:</strong> {date}</p>
                    <p style="margin: 5px 0;"><strong>Time:</strong> {time}</p>
                </div>
                
                <div style="text-align: center; margin: 30px 0;">
                    <a href="{BASE_URL}/video-call/{appointment_id}" 
                       style="background: linear-gradient(135deg, #28a745 0%, #20c997 100%); 
                              color: white; padding: 18px 50px; text-decoration: none; 
                              border-radius: 8px; display: inline-block; font-weight: bold; 
                              font-size: 18px; box-shadow: 0 4px 15px rgba(40, 167, 69, 0.4);">
                        Join Video Call Now
                    </a>
                </div>
                
                <div style="background: #fff3cd; padding: 15px; border-radius: 8px; border-left: 4px solid #ffc107;">
                    <p style="margin: 0; color: #856404;">
                        <strong>📌 Important:</strong> Please join 5 minutes before the scheduled time. 
                        Make sure your camera and microphone are working.
                    </p>
                </div>
            </div>
        </div>
    </body>
    </html>
    """
    
    return send_email(patient_email, subject, body)


def send_doctor_appointment_notification(doctor_email, doctor_name, patient_name, 
                                        date, time, mode, is_emergency=False):
    """
    Send appointment notification email to doctor
    """
    
    emergency_badge = ""
    if is_emergency:
        emergency_badge = """
        <div style="background: #dc3545; color: white; padding: 15px; border-radius: 8px; 
                    margin: 20px 0; text-align: center; font-weight: bold; font-size: 16px;">
            🚨 EMERGENCY APPOINTMENT - Please respond immediately!
        </div>
        """
    
    subject = f"{'🚨 EMERGENCY - ' if is_emergency else ''}New Appointment Booked - MediConnect"
    body = f"""
    <html>
    <head>
        <style>
            body {{ font-family: 'Segoe UI', Arial, sans-serif; line-height: 1.6; color: #333; }}
            .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h2 style="color: #667eea;">New Appointment Booked</h2>
            
            <p>Dear Dr. <strong>{doctor_name}</strong>,</p>
            
            {emergency_badge}
            
            <p>You have a new appointment:</p>
            
            <div style="background: #f8f9fa; padding: 20px; border-radius: 10px; border-left: 4px solid #667eea;">
                <p><strong>Patient:</strong> {patient_name}</p>
                <p><strong>Date:</strong> {date}</p>
                <p><strong>Time:</strong> {time}</p>
                <p><strong>Mode:</strong> {mode.title()}</p>
            </div>
            
            <p style="margin-top: 20px;">
                <a href="{BASE_URL}/doctor/appointments" 
                   style="background: #667eea; color: white; padding: 12px 24px; 
                          text-decoration: none; border-radius: 5px; display: inline-block;">
                    View Appointments
                </a>
            </p>
        </div>
    </body>
    </html>
    """
    
    return send_email(doctor_email, subject, body)


def send_appointment_accepted_email(patient_email, patient_name, doctor_name, 
                                    date, time, mode, appointment_id):
    """
    Send email to patient when doctor accepts/confirms appointment
    """
    
    video_call_section = ""
    if mode in ['online', 'video']:
        video_call_section = f"""
        <div style="text-align: center; margin: 30px 0;">
            <a href="{BASE_URL}/video-call/{appointment_id}" 
               style="background: linear-gradient(135deg, #28a745 0%, #20c997 100%); 
                      color: white; padding: 15px 40px; text-decoration: none; 
                      border-radius: 8px; display: inline-block; font-weight: bold; 
                      font-size: 16px; box-shadow: 0 4px 15px rgba(40, 167, 69, 0.3);">
                🎥 Join Video Consultation
            </a>
        </div>
        """
    
    subject = "✅ Appointment Confirmed by Doctor - MediConnect"
    body = f"""
    <html>
    <head>
        <style>
            body {{ font-family: 'Segoe UI', Arial, sans-serif; line-height: 1.6; color: #333; }}
            .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
            .header {{ background: linear-gradient(135deg, #28a745 0%, #20c997 100%); 
                      color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }}
            .content {{ background: #ffffff; padding: 30px; border: 1px solid #e0e0e0; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1 style="margin: 0; font-size: 28px;">✅ Appointment Confirmed!</h1>
                <p style="margin: 10px 0 0 0; opacity: 0.9;">Your doctor has accepted your appointment</p>
            </div>
            
            <div class="content">
                <p>Dear <strong>{patient_name}</strong>,</p>
                
                <p>Great news! Dr. <strong>{doctor_name}</strong> has confirmed your appointment.</p>
                
                <div style="background: #d4edda; padding: 20px; border-radius: 10px; margin: 20px 0; border-left: 4px solid #28a745;">
                    <h3 style="margin-top: 0; color: #155724;">📋 Confirmed Appointment:</h3>
                    <p style="margin: 5px 0;"><strong>Doctor:</strong> Dr. {doctor_name}</p>
                    <p style="margin: 5px 0;"><strong>Date:</strong> {date}</p>
                    <p style="margin: 5px 0;"><strong>Time:</strong> {time}</p>
                    <p style="margin: 5px 0;"><strong>Mode:</strong> {mode.title()}</p>
                </div>
                
                {video_call_section}
                
                <div style="background: #fff3cd; padding: 15px; border-radius: 8px; margin-top: 20px; border-left: 4px solid #ffc107;">
                    <p style="margin: 0; color: #856404;">
                        <strong>⏰ Reminder:</strong> You will receive a reminder email 5 minutes before your appointment.
                    </p>
                </div>
                
                <p style="margin-top: 20px;">
                    <a href="{BASE_URL}/patient/appointments" 
                       style="color: #667eea; text-decoration: none; font-weight: bold;">
                        View My Appointments →
                    </a>
                </p>
            </div>
        </div>
    </body>
    </html>
    """
    
    return send_email(patient_email, subject, body)


def send_appointment_reminder(email, name, role, doctor_name, patient_name, 
                              date, time, appointment_id, mode):
    """
    Send reminder email 5 minutes before appointment
    
    Args:
        email: Recipient email
        name: Recipient name
        role: 'doctor' or 'patient'
        doctor_name: Doctor's name
        patient_name: Patient's name
        date: Appointment date
        time: Appointment time
        appointment_id: Appointment ID
        mode: Consultation mode
    """
    
    if role == 'patient':
        greeting = f"Dear {name}"
        other_person = f"Dr. {doctor_name}"
        action_text = "Your appointment is starting soon!"
    else:
        greeting = f"Dear Dr. {name}"
        other_person = patient_name
        action_text = "Your patient is waiting!"
    
    video_call_button = ""
    if mode in ['online', 'video']:
        video_call_button = f"""
        <div style="text-align: center; margin: 30px 0;">
            <a href="{BASE_URL}/video-call/{appointment_id}" 
               style="background: linear-gradient(135deg, #dc3545 0%, #c82333 100%); 
                      color: white; padding: 18px 50px; text-decoration: none; 
                      border-radius: 8px; display: inline-block; font-weight: bold; 
                      font-size: 18px; box-shadow: 0 4px 15px rgba(220, 53, 69, 0.4);
                      animation: pulse 2s infinite;">
                🎥 JOIN NOW - Starting in 5 Minutes!
            </a>
        </div>
        """
    
    subject = f"⏰ REMINDER: Appointment in 5 Minutes - MediConnect"
    body = f"""
    <html>
    <head>
        <style>
            body {{ font-family: 'Segoe UI', Arial, sans-serif; line-height: 1.6; color: #333; }}
            .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
            .header {{ background: linear-gradient(135deg, #dc3545 0%, #c82333 100%); 
                      color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }}
            .content {{ background: #ffffff; padding: 30px; border: 1px solid #e0e0e0; }}
            @keyframes pulse {{
                0%, 100% {{ transform: scale(1); }}
                50% {{ transform: scale(1.05); }}
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1 style="margin: 0; font-size: 32px;">⏰ STARTING SOON!</h1>
                <p style="margin: 10px 0 0 0; opacity: 0.9; font-size: 18px;">Your appointment begins in 5 minutes</p>
            </div>
            
            <div class="content">
                <p>{greeting},</p>
                
                <p style="font-size: 18px; font-weight: bold; color: #dc3545;">
                    {action_text}
                </p>
                
                <div style="background: #fff3cd; padding: 20px; border-radius: 10px; margin: 20px 0; border-left: 4px solid #ffc107;">
                    <h3 style="margin-top: 0; color: #856404;">📋 Appointment Details:</h3>
                    <p style="margin: 5px 0;"><strong>Doctor:</strong> Dr. {doctor_name}</p>
                    <p style="margin: 5px 0;"><strong>Patient:</strong> {patient_name}</p>
                    <p style="margin: 5px 0;"><strong>Date:</strong> {date}</p>
                    <p style="margin: 5px 0;"><strong>Time:</strong> {time}</p>
                    <p style="margin: 5px 0;"><strong>Mode:</strong> {mode.title()}</p>
                </div>
                
                {video_call_button}
                
                <div style="background: #d1ecf1; padding: 15px; border-radius: 8px; margin-top: 20px; border-left: 4px solid #17a2b8;">
                    <p style="margin: 0; color: #0c5460;">
                        <strong>💡 Tip:</strong> Make sure your camera and microphone are working properly.
                    </p>
                </div>
            </div>
        </div>
    </body>
    </html>
    """
    
    return send_email(email, subject, body)


def send_doctor_verification_email(doctor_email, doctor_name, verification_id, status, notes=""):
    """
    Send email notification when doctor verification status changes
    
    Args:
        doctor_email: Doctor's email address
        doctor_name: Doctor's name
        verification_id: Doctor's verification ID (e.g., DOC-2026-6550)
        status: 'approved' or 'rejected'
        notes: Additional notes from admin (optional)
    """
    
    if status == 'approved':
        subject = "✅ Account Verified - Welcome to MediConnect!"
        header_color = "linear-gradient(135deg, #28a745 0%, #20c997 100%)"
        status_icon = "✅"
        status_text = "Congratulations! Your account has been verified"
        message_content = f"""
        <p>Dear Dr. <strong>{doctor_name}</strong>,</p>
        
        <p>Excellent news! Your doctor account has been successfully verified by our admin team.</p>
        
        <div style="background: #d4edda; padding: 20px; border-radius: 10px; margin: 20px 0; border-left: 4px solid #28a745;">
            <h3 style="margin-top: 0; color: #155724;">🎉 Account Status: VERIFIED</h3>
            <p style="margin: 5px 0;"><strong>Verification ID:</strong> {verification_id}</p>
            <p style="margin: 5px 0;"><strong>Status:</strong> Active & Ready</p>
            {f'<p style="margin: 5px 0;"><strong>Admin Notes:</strong> {notes}</p>' if notes else ''}
        </div>
        
        <div style="text-align: center; margin: 30px 0;">
            <a href="{BASE_URL}/doctor/login" 
               style="background: linear-gradient(135deg, #28a745 0%, #20c997 100%); 
                      color: white; padding: 18px 50px; text-decoration: none; 
                      border-radius: 8px; display: inline-block; font-weight: bold; 
                      font-size: 18px; box-shadow: 0 4px 15px rgba(40, 167, 69, 0.4);">
                🚀 Login to Your Dashboard
            </a>
        </div>
        
        <div style="background: #e3f2fd; padding: 20px; border-radius: 10px; margin: 20px 0; border-left: 4px solid #2196f3;">
            <h4 style="margin-top: 0; color: #1565c0;">🏥 What You Can Do Now:</h4>
            <ul style="margin: 10px 0; padding-left: 20px; color: #1565c0;">
                <li>Accept and manage patient appointments</li>
                <li>Conduct video consultations</li>
                <li>View patient medical history</li>
                <li>Update your availability and consultation fees</li>
                <li>Access your doctor dashboard</li>
            </ul>
        </div>
        
        <p style="margin-top: 30px;">
            Welcome to the MediConnect family! We're excited to have you on board and look forward to the excellent care you'll provide to our patients.
        </p>
        """
        
    else:  # rejected
        subject = "❌ Account Verification Update - MediConnect"
        header_color = "linear-gradient(135deg, #dc3545 0%, #c82333 100%)"
        status_icon = "❌"
        status_text = "Account verification was not approved"
        rejection_reason = notes if notes else "Documents did not meet verification requirements"
        
        message_content = f"""
        <p>Dear Dr. <strong>{doctor_name}</strong>,</p>
        
        <p>Thank you for your interest in joining MediConnect. After careful review, we were unable to approve your account verification at this time.</p>
        
        <div style="background: #f8d7da; padding: 20px; border-radius: 10px; margin: 20px 0; border-left: 4px solid #dc3545;">
            <h3 style="margin-top: 0; color: #721c24;">📋 Verification Details:</h3>
            <p style="margin: 5px 0;"><strong>Verification ID:</strong> {verification_id}</p>
            <p style="margin: 5px 0;"><strong>Status:</strong> Not Approved</p>
            <p style="margin: 5px 0;"><strong>Reason:</strong> {rejection_reason}</p>
        </div>
        
        <div style="background: #fff3cd; padding: 20px; border-radius: 10px; margin: 20px 0; border-left: 4px solid #ffc107;">
            <h4 style="margin-top: 0; color: #856404;">📞 Next Steps:</h4>
            <p style="margin: 10px 0; color: #856404;">
                If you believe this decision was made in error or if you have additional documentation to provide, 
                please contact our admin team for further assistance.
            </p>
            <p style="margin: 10px 0; color: #856404;">
                <strong>Contact:</strong> admin@mediconnect.com<br>
                <strong>Reference:</strong> {verification_id}
            </p>
        </div>
        
        <p style="margin-top: 30px;">
            We appreciate your understanding and encourage you to reach out if you have any questions about this decision.
        </p>
        """
    
    body = f"""
    <html>
    <head>
        <style>
            body {{ font-family: 'Segoe UI', Arial, sans-serif; line-height: 1.6; color: #333; }}
            .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
            .header {{ background: {header_color}; 
                      color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }}
            .content {{ background: #ffffff; padding: 30px; border: 1px solid #e0e0e0; }}
            .footer {{ background: #f8f9fa; padding: 20px; text-align: center; 
                      border-radius: 0 0 10px 10px; color: #666; font-size: 12px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1 style="margin: 0; font-size: 32px;">{status_icon} Doctor Verification</h1>
                <p style="margin: 10px 0 0 0; opacity: 0.9; font-size: 18px;">{status_text}</p>
            </div>
            
            <div class="content">
                {message_content}
            </div>
            
            <div class="footer">
                <p style="margin: 0;">MediConnect Healthcare Management System</p>
                <p style="margin: 10px 0 0 0;">
                    This is an automated email. For support, contact admin@mediconnect.com
                </p>
            </div>
        </div>
    </body>
    </html>
    """
    
    return send_email(doctor_email, subject, body)


# Print configuration status on import
if __name__ != "__main__":
    if EMAIL_ENABLED:
        print(f"[Email] [SUCCESS] Email notifications enabled (sending from: {GMAIL_USER})")
    else:
        print("[Email] [WARNING] Email notifications disabled. Configure GMAIL_USER and GMAIL_PASSWORD in .env")
