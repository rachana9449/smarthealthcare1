# Testing Guide - New Features

## 🎯 Features to Test

### 1. Online/Offline Appointment Booking

**Steps:**
1. Login as a patient
2. Go to "Consult Doctor"
3. Select any doctor and click "Book Appointment"
4. **NEW**: You'll see a dropdown for "Consultation Type"
   - Select "🏥 In-Person (Offline)" OR
   - Select "💻 Online Video Call"
5. Fill in date, time, and reason
6. Submit booking

**Expected Result:**
- Appointment is created with the selected consultation type
- Doctor receives notification with consultation type mentioned

---

### 2. Video Call for Online Appointments

**Steps:**
1. Login as doctor
2. Go to "Appointments"
3. Find a pending appointment (should show consultation type badge)
4. Click "Accept" button
5. **For online appointments**: "Start Video Call" button appears
6. Click "Start Video Call"

**Expected Result:**
- Jitsi Meet video call opens in full screen
- Patient can join from their appointments page
- After ending call, doctor is prompted to add prescription

---

### 3. Adding Prescription After Consultation

**Steps:**
1. After video call ends (or from confirmed appointments)
2. Doctor clicks "Add Prescription" button
3. Fill in the form:
   - **Diagnosis**: e.g., "Viral Fever"
   - **Prescription**: 
     ```
     1. Paracetamol 500mg - 1 tablet twice daily (5 days)
     2. Vitamin C 500mg - 1 tablet once daily (7 days)
     ```
   - **Lab Tests**:
     ```
     1. Complete Blood Count (CBC)
     2. Blood Sugar (Fasting)
     ```
4. Click "Save Prescription & Notify Patient"

**Expected Result:**
- Prescription saved to appointment
- Patient receives notification
- Appointment status changes to "completed"

---

### 4. Patient Views Prescription

**Steps:**
1. Login as patient
2. Go to "My Appointments"
3. Find completed appointment
4. Click "View Details" button

**Expected Result:**
- Modal opens showing:
  - Doctor name and specialization
  - Diagnosis
  - Complete prescription
  - Lab test recommendations
  - **"Find Nearby Pharmacies"** button
  - **"Find Nearby Diagnostic Centers"** button

---

### 5. Finding Nearby Services

**Steps:**
1. From prescription modal, click "Find Nearby Pharmacies"
2. OR click "Find Nearby Diagnostic Centers"
3. OR go to Dashboard → "Nearby Services"

**Expected Result:**
- Redirects to nearby services page
- Shows relevant services based on prescription:
  - Pharmacies (if medicines prescribed)
  - Diagnostic centers (if lab tests recommended)
  - Hospitals (if CT scan or procedures needed)

---

## 🧪 Test Scenarios

### Scenario 1: Complete Online Consultation Flow
1. Patient books **online** appointment
2. Doctor accepts appointment
3. Both join video call
4. Doctor ends call and adds prescription
5. Patient views prescription
6. Patient finds nearby pharmacy
7. Patient gets medicines

### Scenario 2: Offline Appointment with Lab Tests
1. Patient books **offline** appointment
2. Doctor accepts appointment
3. Patient visits clinic in person
4. Doctor adds prescription with lab tests
5. Patient views prescription
6. Patient finds nearby diagnostic center
7. Patient gets tests done

### Scenario 3: Emergency Online Consultation
1. Patient books **online** appointment
2. Check "This is an EMERGENCY" checkbox
3. Doctor receives urgent notification
4. Doctor accepts immediately
5. Video call for emergency consultation
6. Doctor prescribes immediate medication
7. Patient finds 24/7 pharmacy nearby

---

## ✅ Verification Checklist

### Appointment Booking:
- [ ] Can select online/offline consultation type
- [ ] Consultation type is saved correctly
- [ ] Doctor sees consultation type in appointments list

### Video Call:
- [ ] Video call button only shows for online appointments
- [ ] Video call opens correctly
- [ ] Both doctor and patient can join
- [ ] After call, doctor is prompted for prescription

### Prescription Management:
- [ ] Doctor can add diagnosis
- [ ] Doctor can add medicines
- [ ] Doctor can add lab tests
- [ ] Prescription is saved correctly
- [ ] Patient receives notification

### Patient View:
- [ ] Patient can view prescription details
- [ ] "Find Nearby Pharmacies" button works
- [ ] "Find Nearby Diagnostic Centers" button works
- [ ] Prescription is readable and well-formatted

### Notifications:
- [ ] Patient notified when prescription is added
- [ ] Notification mentions nearby services
- [ ] Notification type is correct (prescription)

---

## 🐛 Common Issues & Solutions

### Issue: Video call button not showing
**Solution**: Make sure appointment is:
1. Accepted by doctor (status = 'confirmed')
2. Marked as 'online' consultation type

### Issue: Prescription not saving
**Solution**: Check that:
1. You're logged in as a doctor
2. Appointment ID is valid
3. Database migration was run successfully

### Issue: Nearby services not showing
**Solution**: 
1. Check if nearby_services.py is working
2. Verify Google Maps API key is configured
3. Check browser location permissions

### Issue: Can't join video call
**Solution**:
1. Check internet connection
2. Allow camera/microphone permissions
3. Try different browser (Chrome recommended)

---

## 📊 Test Data Examples

### Sample Prescription:
```
1. Amoxicillin 500mg - 1 capsule three times daily after meals (7 days)
2. Paracetamol 650mg - 1 tablet when needed for fever (max 3 per day)
3. Cetirizine 10mg - 1 tablet once daily at bedtime (5 days)
4. Vitamin D3 60000 IU - 1 capsule once weekly (4 weeks)
```

### Sample Lab Tests:
```
1. Complete Blood Count (CBC)
2. Erythrocyte Sedimentation Rate (ESR)
3. C-Reactive Protein (CRP)
4. Chest X-Ray (PA View)
5. Blood Sugar - Fasting & PP
```

### Sample Diagnosis:
```
Upper Respiratory Tract Infection with mild fever
```

---

## 🎬 Demo Flow

**For Presentation:**

1. **Show booking**: "Patient can now choose online or offline consultation"
2. **Show video call**: "For online appointments, both can join video call"
3. **Show prescription**: "After consultation, doctor adds prescription"
4. **Show patient view**: "Patient sees prescription with nearby services"
5. **Show nearby services**: "One click to find pharmacies and labs"

---

## 📞 Need Help?

- Check `FEATURE_UPDATE_SUMMARY.md` for detailed documentation
- Review `QUICK_REFERENCE.md` for system overview
- Check `TESTING_GUIDE.md` for general testing procedures

**Status**: Ready for testing ✅
**Last Updated**: May 4, 2026
