# 🏥 Smart Healthcare System

A comprehensive healthcare management system with controlled doctor registration, prescription management, and nearby services finder.

---

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Initialize Database
```bash
python add_verification_column.py
python add_prescription_columns.py
```

### 3. Create Admin Account
```bash
python create_admin.py
```

### 4. Start Application
```bash
python app.py
```

### 5. Access System
Open browser: **http://localhost:5000**

---

## 🔐 Default Credentials

### Admin Login
- **URL**: http://localhost:5000/login-admin
- **Email**: admin@test.com
- **Password**: admin123

---

## ✨ Key Features

### 1. 🔐 Controlled Doctor Registration
- Auto-generated verification IDs (DOC-2026-XXXX)
- Admin approval required
- Secure temporary passwords
- Email and phone uniqueness

**How it works:**
1. Doctor registers at `/signup-doctor`
2. Gets verification ID and temp password
3. Status: Pending (inactive)
4. Admin verifies at `/admin/verify-doctors`
5. Doctor becomes active

### 2. 👨‍💼 Admin Verification Dashboard
- View pending registrations
- Verify/reject doctors
- Manage verified doctors
- Statistics overview

**Access**: `/admin/verify-doctors`

### 3. 💊 Prescription Management
- Doctors add prescriptions
- Patients view prescriptions
- Print functionality
- Auto-notifications

**Doctor workflow:**
1. Go to appointments
2. Click "Add Prescription"
3. Enter medicines and lab tests
4. Save → Patient notified

**Patient workflow:**
1. Go to appointments
2. Click "View Prescription"
3. See medicines and lab tests
4. Print if needed

### 4. 🗺️ Nearby Services Finder
- Find medical stores
- Find diagnostic labs
- Find CT scan centers
- Location-based search
- Google Maps integration

**Access from prescription page:**
- "Find Nearby Medical Stores"
- "Find Nearby Labs"
- "Find CT Scan Centers"
- "Find All Nearby Services"

### 5. 📅 Appointment Management
- Book appointments
- Video consultations
- Reschedule/cancel
- Status tracking

### 6. 🔔 Real-time Notifications
- Email notifications
- In-app notifications
- SSE for real-time updates

---

## 📁 Project Structure

```
smarthealthcare/
├── app.py                              # Main Flask application
├── enhancements.py                     # Additional features
├── requirements.txt                    # Python dependencies
├── medical.db                          # SQLite database
│
├── templates/                          # HTML templates
│   ├── base.html                       # Base template
│   ├── landing.html                    # Landing page
│   ├── doctor_registration.html        # Doctor registration
│   ├── add_prescription.html           # Add prescription form
│   ├── view_prescription.html          # View prescription
│   ├── admin_verify_doctors.html       # Verification dashboard
│   └── ...                             # Other templates
│
├── static/                             # Static files
│   ├── uploads/                        # Uploaded files
│   └── manifest.json                   # PWA manifest
│
├── docs/                               # Documentation
│   └── ...                             # Feature docs
│
├── Scripts/                            # Utility scripts
│   ├── create_admin.py                 # Create admin account
│   ├── add_verification_column.py      # DB migration
│   ├── add_prescription_columns.py     # DB migration
│   ├── create_sample_data.py           # Sample data
│   └── train_model.py                  # ML model training
│
└── README.md                           # This file
```

---

## 🗄️ Database Schema

### Key Tables

**users** - All system users
- id, name, email, password, role, phone, address, age, gender

**doctors** - Doctor-specific data
- id, user_id, specialization, qualification, experience
- consultation_fee, available
- **verification_id**, **verification_status** (NEW)

**patients** - Patient-specific data
- id, user_id, blood_group, medical_history

**appointments** - Appointment records
- id, patient_id, doctor_id, appointment_date, appointment_time
- status, reason, notes, consultation_type
- **prescription**, **lab_tests** (NEW)

**consultations** - Consultation records
- id, patient_id, doctor_id, symptoms, diagnosis
- prescription, status, consultation_date

**notifications** - User notifications
- id, user_id, title, message, type, is_read

---

## 🎯 User Roles

### 1. Admin
**Access**: Full system control

**Features:**
- Verify doctors
- Manage users
- View consultations
- Generate reports
- System settings

### 2. Doctor
**Access**: Medical services

**Features:**
- View appointments
- Add prescriptions
- Conduct consultations
- Manage availability
- View feedback

### 3. Patient
**Access**: Healthcare services

**Features:**
- Book appointments
- View prescriptions
- Find nearby services
- Consultation history
- Medical records

---

## 🔧 Configuration

### Email Settings (Optional)
Configure in `.env` file:
```
GMAIL_USER=your-email@gmail.com
GMAIL_PASSWORD=your-app-password
```

### Database Migrations
Run migrations when needed:
```bash
python add_verification_column.py
python add_prescription_columns.py
```

---

## 🧪 Testing

### Test Controlled Registration
```bash
1. Visit /signup-doctor
2. Register a test doctor
3. Login as admin
4. Verify the doctor
5. Doctor can now login and work
```

### Test Prescription System
```bash
1. Login as doctor
2. Add prescription to appointment
3. Login as patient
4. View prescription
5. Find nearby services
```

---

## 📊 Features Overview

| Feature | Doctor | Patient | Admin |
|---------|--------|---------|-------|
| Registration | ✅ | ✅ | - |
| Verification | - | - | ✅ |
| Appointments | ✅ | ✅ | ✅ |
| Prescriptions | ✅ (Add) | ✅ (View) | ✅ |
| Nearby Services | - | ✅ | - |
| Consultations | ✅ | ✅ | ✅ |
| Reports | - | - | ✅ |
| User Management | - | - | ✅ |

---

## 🔐 Security Features

✅ **Password Security**
- Hashed passwords (werkzeug)
- Secure token generation
- Temporary passwords for doctors

✅ **Access Control**
- Role-based access
- Session management
- Login required decorators

✅ **Data Validation**
- Server-side validation
- Client-side validation
- SQL injection protection

✅ **Controlled Registration**
- Admin approval required
- Verification tracking
- Inactive by default

---

## 📱 API Endpoints

### Authentication
- POST `/login-doctor` - Doctor login
- POST `/login-patient` - Patient login
- POST `/login-admin` - Admin login
- GET `/logout` - Logout

### Registration
- POST `/register-doctor` - Doctor registration API
- POST `/signup-doctor` - Doctor signup form
- POST `/signup-patient` - Patient signup form

### Appointments
- GET `/patient/book-appointment/<doctor_id>` - Book appointment
- GET `/patient/appointments` - View appointments
- GET `/doctor/appointments` - Doctor appointments
- POST `/appointment/add-prescription/<id>` - Add prescription

### Prescriptions
- GET `/appointment/view-prescription/<id>` - View prescription
- GET `/nearby-services` - Find nearby services

### Admin
- GET `/admin/verify-doctors` - Verification dashboard
- POST `/admin/verify-doctor/<id>` - Verify/reject doctor

---

## 🎨 UI Features

✅ **Modern Design**
- Gradient backgrounds
- Card-based layouts
- Responsive design
- Bootstrap 5

✅ **User Experience**
- Loading states
- Success/error messages
- Copy to clipboard
- Print functionality

✅ **Accessibility**
- Clear labels
- Keyboard navigation
- Screen reader friendly

---

## 📚 Documentation

Detailed documentation available in `/docs`:
- `CONTROLLED_REGISTRATION_GUIDE.md` - Registration system
- `PRESCRIPTION_FEATURE_COMPLETE.md` - Prescription features
- `PROJECT_DOCUMENTATION.md` - Complete project docs

---

## 🐛 Troubleshooting

### Server won't start
```bash
# Check if port 5000 is in use
netstat -ano | findstr :5000

# Kill the process if needed
taskkill /PID <process_id> /F
```

### Database errors
```bash
# Run migrations
python add_verification_column.py
python add_prescription_columns.py

# Or recreate database
# Delete medical.db and restart app
```

### Admin login not working
```bash
# Recreate admin account
python create_admin.py
```

---

## 🚀 Deployment

### Production Checklist
- [ ] Change secret key in app.py
- [ ] Update admin credentials
- [ ] Configure email settings
- [ ] Set up HTTPS
- [ ] Use production WSGI server (gunicorn)
- [ ] Set DEBUG=False
- [ ] Configure database backups

---

## 📞 Support

For issues or questions:
1. Check documentation in `/docs`
2. Review error logs in console
3. Check database with `check_db.py`

---

## 📝 License

Part of Smart Healthcare System - Medical Management Platform

---

## ✅ System Status

**Version**: 2.1.0  
**Status**: ✅ Production Ready  
**Last Updated**: 2026  

**Features:**
- ✅ Controlled Registration
- ✅ Admin Verification
- ✅ Prescription Management
- ✅ Nearby Services Finder
- ✅ Appointment System
- ✅ Real-time Notifications

---

**Built with ❤️ for better healthcare management**
