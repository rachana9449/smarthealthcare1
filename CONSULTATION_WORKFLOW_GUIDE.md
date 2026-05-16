# Consultation Workflow Guide

## ✅ **Your Requested Workflow is Already Implemented!**

The system already has the complete consultation workflow you described:

### 📋 **Complete Workflow:**

```
1. Patient Books Appointment
   ↓
2. Doctor Confirms Appointment
   ↓
3. Video Call (Jitsi Meet)
   ↓
4. Doctor Ends Call → Prompted to Add Prescription
   ↓
5. Doctor Adds Prescription & Lab Tests
   ↓
6. Patient Gets Notification
   ↓
7. Patient Views Prescription
   ↓
8. Patient Finds Nearby Services:
   - Medical Stores (Pharmacies)
   - Diagnostic Labs
   - CT Scan Centers
```

---

## 🎥 **Step 1: Video Call**

### **How to Start:**

**For Patients:**
1. Go to "My Appointments"
2. Find a **Confirmed** appointment
3. Click **"Join Video Call"** button (green button)
4. Video call opens in full screen

**For Doctors:**
1. Go to "My Appointments"
2. Find a **Confirmed** appointment
3. Click **"Join Video Call"** button
4. Video call opens in full screen

### **During Video Call:**
- Full-screen Jitsi Meet interface
- Audio/Video controls
- Chat functionality
- Screen sharing
- Top bar shows:
  - Doctor name
  - Patient name
  - Appointment date & time
  - "End Call" button

### **Ending the Call:**

**For Doctors:**
- Click "End Call" button
- **Automatic prompt appears:** "Would you like to add prescription and lab test recommendations for this patient?"
- Click **"OK"** → Redirected to Add Prescription page
- Click **"Cancel"** → Redirected to Appointments page

**For Patients:**
- Click "End Call" button
- Redirected to Appointments page
- Wait for doctor to add prescription

---

## 💊 **Step 2: Doctor Adds Prescription**

### **Add Prescription Page:**

**URL:** `/appointment/add-prescription/<appointment_id>`

**Form Fields:**
1. **Prescription** (Medicines):
   - Text area for medicine details
   - Dosage, frequency, duration
   - Example: "Paracetamol 500mg - 1 tablet twice daily for 3 days"

2. **Lab Tests** (Optional):
   - Text area for recommended tests
   - Example: "Complete Blood Count (CBC), Blood Sugar Test"

3. **Submit Button:**
   - Saves prescription
   - Marks appointment as "Completed"
   - Sends notification to patient

### **What Happens After Submission:**

1. ✅ Prescription saved to database
2. ✅ Appointment status → "Completed"
3. ✅ Patient receives notification:
   - 💊 "Prescription Ready" (if medicines prescribed)
   - 🔬 "Lab Tests Recommended" (if tests prescribed)
   - 🏥 "Prescription & Tests Ready" (if both)
4. ✅ Doctor redirected to Appointments page

---

## 📋 **Step 3: Patient Views Prescription**

### **How to Access:**

**Method 1: From Appointments Page**
1. Go to "My Appointments"
2. Find the **Completed** appointment
3. Click **"View Prescription"** button (green button)

**Method 2: From Notifications**
1. Click notification bell (top right)
2. Click on prescription notification
3. Opens prescription page

### **Prescription Page Features:**

#### **Top Section:**
- Doctor name & specialization
- Appointment date & time
- Reason for visit
- Diagnosis/Notes

#### **Prescribed Medicines Section:**
- 💊 Green card with medicine details
- **"Find Nearby Medical Stores"** button
- **"Print Prescription"** button

#### **Lab Tests Section:**
- 🔬 Blue card with test details
- **"Find Nearby Labs"** button
- **"Find CT Scan Centers"** button

#### **Quick Service Cards:**
Three clickable cards:
1. **Medical Stores** (Green) - Find pharmacies
2. **Diagnostic Labs** (Blue) - Find labs
3. **CT Scan Centers** (Cyan) - Find imaging centers

#### **Find All Services:**
- If both prescription and lab tests exist
- Purple gradient button
- **"Find All Nearby Services"** - Shows everything

---

## 🗺️ **Step 4: Find Nearby Services**

### **Service Types Available:**

1. **Medical Stores (Pharmacies)**
   - For prescribed medicines
   - Shows nearby pharmacies
   - Google Maps integration

2. **Diagnostic Labs**
   - For blood tests, urine tests, etc.
   - Shows nearby diagnostic centers
   - Lab test facilities

3. **CT Scan Centers**
   - For imaging tests
   - CT scan facilities
   - X-ray centers
   - MRI centers

4. **All Services**
   - Shows all three types together
   - One-stop view

### **Nearby Services Page Features:**

- 📍 Location-based search
- 🗺️ Google Maps integration
- 📞 Contact information
- 🏥 Service details
- 📏 Distance from user
- ⭐ Ratings (if available)

---

## 🔔 **Notifications System**

### **Patient Receives:**

**After Doctor Adds Prescription:**
- Notification appears in bell icon (top right)
- Red badge shows unread count
- Click to view notification
- Click notification to go to prescription

**Notification Types:**
- 💊 Prescription Ready
- 🔬 Lab Tests Recommended
- 🏥 Prescription & Tests Ready

---

## 📱 **How to Test the Complete Workflow**

### **Test as Doctor:**

1. **Login as Doctor**
   - Use doctor credentials

2. **Go to Appointments**
   - Find a confirmed appointment
   - Or confirm a pending appointment first

3. **Start Video Call**
   - Click "Join Video Call"
   - Video call opens

4. **End Call**
   - Click "End Call" button
   - Prompt appears: "Add prescription?"
   - Click "OK"

5. **Add Prescription**
   - Fill in medicines:
     ```
     Paracetamol 500mg - 1 tablet twice daily for 3 days
     Amoxicillin 250mg - 1 capsule three times daily for 5 days
     ```
   - Fill in lab tests:
     ```
     Complete Blood Count (CBC)
     Blood Sugar Test (Fasting)
     ```
   - Click "Submit"

6. **Verify**
   - Check appointment status → "Completed"
   - Patient should receive notification

### **Test as Patient:**

1. **Login as Patient**
   - Use patient credentials

2. **Check Notifications**
   - Click bell icon (top right)
   - Should see prescription notification
   - Click notification

3. **View Prescription**
   - Or go to Appointments → Click "View Prescription"
   - See medicines and lab tests
   - See nearby services buttons

4. **Find Nearby Services**
   - Click "Find Nearby Medical Stores"
   - See pharmacies on map
   - Click "Find Nearby Labs"
   - See diagnostic centers
   - Click "Find CT Scan Centers"
   - See imaging facilities

---

## 🎯 **Key Features**

### **Video Call:**
- ✅ Full-screen Jitsi Meet
- ✅ Audio/Video controls
- ✅ Chat functionality
- ✅ Screen sharing
- ✅ Same room for doctor & patient
- ✅ Automatic prescription prompt for doctor

### **Prescription:**
- ✅ Medicines with dosage
- ✅ Lab test recommendations
- ✅ Diagnosis/Notes
- ✅ Print functionality
- ✅ Automatic notifications

### **Nearby Services:**
- ✅ Medical stores finder
- ✅ Diagnostic labs finder
- ✅ CT scan centers finder
- ✅ Google Maps integration
- ✅ Location-based search
- ✅ Contact information

### **Notifications:**
- ✅ Real-time notifications
- ✅ Unread badge counter
- ✅ Click to view prescription
- ✅ Different icons for different types

---

## 📂 **Relevant Files**

### **Templates:**
- `video_call.html` - Video call interface
- `add_prescription.html` - Doctor adds prescription
- `view_prescription.html` - Patient views prescription
- `nearby_services.html` - Find nearby services

### **Routes (app.py):**
- `/video-call/<appointment_id>` - Start video call
- `/appointment/add-prescription/<appointment_id>` - Add prescription
- `/appointment/view-prescription/<appointment_id>` - View prescription
- `/nearby-services` - Find nearby services

### **Database:**
- `appointments` table has:
  - `prescription` column - Stores medicines
  - `lab_tests` column - Stores test recommendations
  - `status` column - Tracks appointment status

---

## 🚀 **Quick Start**

### **To Test Right Now:**

1. **Create a Test Appointment:**
   - Login as patient
   - Book appointment with a doctor
   - Login as doctor
   - Confirm the appointment

2. **Start Video Call:**
   - Both patient and doctor can join
   - Test the video call features

3. **Add Prescription:**
   - Doctor ends call
   - Clicks "OK" on prompt
   - Fills prescription form
   - Submits

4. **View & Find Services:**
   - Patient checks notifications
   - Views prescription
   - Clicks nearby services buttons
   - Sees medical stores, labs, CT centers

---

## ✅ **Everything is Already Working!**

**Your requested workflow is 100% implemented:**

1. ✅ Video call between doctor and patient
2. ✅ After call ends, doctor adds prescription
3. ✅ Patient can view prescription
4. ✅ Patient can find nearby:
   - Medical stores
   - Diagnostic labs
   - CT scan centers
5. ✅ Notifications system
6. ✅ Print prescription
7. ✅ Google Maps integration

**No additional development needed!**

Just test the workflow with the steps above! 🎉

---

## 📞 **Need Help?**

If you encounter any issues:
1. Check appointment status (must be "Confirmed" for video call)
2. Verify prescription was added by doctor
3. Check notifications are enabled
4. Ensure location services are enabled for nearby services

**The system is ready to use!** 🚀✨
