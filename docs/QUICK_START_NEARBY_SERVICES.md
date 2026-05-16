# 🚀 Quick Start: Nearby Medical Services

## ✅ Feature is Ready to Use!

The Nearby Medical Services feature is **fully functional** and requires **NO API keys** to get started!

---

## 🎯 How It Works

### **For Doctors:**
1. Complete a consultation
2. Add prescription (medicines and/or tests)
3. Set status to "Completed"
4. **System automatically notifies patient** about nearby services!

### **For Patients:**
1. Receive notification after consultation
2. Click notification or go to Consultation History
3. Click "Find Medical Store" or "Find Diagnostic Lab"
4. Allow location access (or enter address)
5. **View nearby services with directions!**

---

## 🧪 Test the Feature

### **Step 1: Create Test Data**

#### Login as Doctor:
```
Email: doctor@test.com
Password: [your password]
```

#### Complete a Consultation:
```
Diagnosis: Common Cold
Prescription:
  Paracetamol 500mg - 1-0-1 (3 days)
  Vitamin C - 0-0-1 (7 days)
  Blood Test - CBC, ESR
  
Status: Completed
```

### **Step 2: Login as Patient**
```
Email: patient@test.com
Password: [your password]
```

### **Step 3: Check Notifications**
- You'll see: "💊 Prescription Ready - Find Nearby Services"
- Click the notification

### **Step 4: Find Services**
- Click "Find Medical Stores" or "Find Diagnostic Labs"
- Allow location access when prompted
- View results on map!

---

## 📍 Sample Locations to Test

### **India**
```
Bangalore: 12.9716, 77.5946
Mumbai: 19.0760, 72.8777
Delhi: 28.6139, 77.2090
```

### **USA**
```
New York: 40.7128, -74.0060
Los Angeles: 34.0522, -118.2437
Chicago: 41.8781, -87.6298
```

### **Europe**
```
London: 51.5074, -0.1278
Paris: 48.8566, 2.3522
Berlin: 52.5200, 13.4050
```

---

## 🔧 Configuration (Optional)

### **Use Google Places API for Enhanced Results**

1. **Get API Key:**
   - Go to: https://console.cloud.google.com/apis/credentials
   - Create new project
   - Enable "Places API"
   - Create credentials (API Key)

2. **Add to .env:**
   ```bash
   GOOGLE_PLACES_API_KEY=AIzaSyC...your_key_here
   ```

3. **Restart Application:**
   ```bash
   python app.py
   ```

**Benefits:**
- ⭐ Service ratings
- 📸 Photos
- 💬 Reviews
- 🕒 Real-time open/closed status
- 📞 Verified phone numbers

---

## 🎨 Customization

### **Change Search Radius**

Edit `app.py`:
```python
def find_nearby_pharmacies(lat, lng, radius=5000):  # 5 km
    # Change to 10000 for 10 km
```

### **Add More Test Keywords**

Edit `analyze_prescription_type()` in `app.py`:
```python
diagnostic_keywords = [
    'ct scan', 'mri', 'x-ray',
    # Add your keywords here
    'pet scan', 'bone density', 'stress test'
]
```

### **Customize Notifications**

Edit `doctor_consultations()` in `app.py`:
```python
notification_title = '💊 Your Custom Title'
notification_message = 'Your custom message...'
```

---

## 📊 Sample Prescriptions for Testing

### **Medicines Only:**
```
Paracetamol 500mg - 1-0-1 after food (5 days)
Amoxicillin 250mg - 1-1-1 before food (7 days)
Cetirizine 10mg - 0-0-1 at bedtime (3 days)
```
**Expected:** Suggests "Find Medical Stores"

### **Tests Only:**
```
Blood Tests:
- Complete Blood Count (CBC)
- Lipid Profile
- Liver Function Test (LFT)

Imaging:
- Chest X-Ray
- Abdominal Ultrasound
```
**Expected:** Suggests "Find Diagnostic Labs"

### **Both Medicines and Tests:**
```
Medicines:
- Metformin 500mg - 1-0-1 (30 days)
- Aspirin 75mg - 0-0-1 (30 days)

Tests:
- HbA1c (Diabetes Test)
- Fasting Blood Sugar
- ECG
```
**Expected:** Suggests "Find Both Services"

---

## 🐛 Common Issues

### **"Location not detected"**
✅ **Solution:** Click "Use my current location" and allow browser permission

### **"No services found"**
✅ **Solution:** 
- Try a different location (use sample coordinates above)
- Check if you're in a populated area
- OpenStreetMap may have limited data in some regions

### **"Map not loading"**
✅ **Solution:**
- Check internet connection
- Disable ad blockers
- Try different browser

---

## 📱 Mobile Testing

### **On Mobile Device:**
1. Open app in mobile browser
2. GPS will automatically detect location
3. Tap service cards to view on map
4. Tap phone numbers to call directly
5. Tap "Directions" for Google Maps navigation

---

## 🎯 Success Criteria

✅ Doctor can complete consultation with prescription  
✅ Patient receives automatic notification  
✅ Patient can view nearby services  
✅ Location detection works (GPS or manual)  
✅ Services displayed with distance and details  
✅ Map shows service locations  
✅ Directions button opens Google Maps  
✅ Call button works on mobile  

---

## 📈 Monitoring

### **Check Logs:**
```bash
# Watch for prescription analysis
[INFO] Prescription analyzed: type=pharmacy, medicines=3, tests=0

# Watch for service search
[INFO] Searching for pharmacies near: 12.9716, 77.5946
[INFO] Found 8 pharmacies within 5 km
```

### **Database Queries:**
```sql
-- Check notifications sent
SELECT * FROM notifications 
WHERE type = 'prescription' 
ORDER BY created_at DESC 
LIMIT 10;

-- Check completed consultations
SELECT * FROM consultations 
WHERE status = 'completed' 
AND prescription IS NOT NULL 
ORDER BY consultation_date DESC;
```

---

## 🎉 You're All Set!

The feature is **production-ready** and works without any API keys!

### **Next Steps:**
1. Test with sample prescriptions
2. Verify notifications are sent
3. Check location detection works
4. Ensure map displays correctly
5. Test on mobile devices

### **Optional Enhancements:**
- Add Google Places API key for ratings
- Customize search radius
- Add more test keywords
- Translate to local language

---

## 📞 Need Help?

- Check `docs/NEARBY_SERVICES_FEATURE.md` for detailed documentation
- Review console logs for errors
- Test with sample data provided above
- Verify database has consultation records

---

**Happy Testing! 🎊**
