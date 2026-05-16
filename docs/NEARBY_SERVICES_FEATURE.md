# 🏥 Intelligent Nearby Medical Services Feature

## Overview

This feature automatically suggests nearby medical stores and diagnostic labs to patients based on their doctor's prescription. It's an intelligent healthcare assistant that analyzes prescriptions and provides location-based recommendations.

---

## 🎯 Key Features

### 1. **Automatic Prescription Analysis**
- Analyzes prescription text to identify:
  - **Medicines** (tablets, capsules, syrups, injections)
  - **Diagnostic Tests** (CT scan, MRI, blood tests, X-rays, etc.)
- Determines service type: `pharmacy`, `diagnostic`, or `both`

### 2. **Smart Notifications**
When a doctor completes a consultation with a prescription:
- Patient receives an automatic notification
- Notification includes smart suggestions based on prescription content
- Direct link to find nearby services

### 3. **Location-Based Search**
- **GPS Detection**: Automatically detects patient's current location
- **Manual Input**: Patients can enter address or pincode
- **Radius Search**: Finds services within 5-10 km radius
- **Expandable Search**: Automatically expands to 25 km if no results found

### 4. **Service Discovery**
Uses **OpenStreetMap Overpass API** (free, no API key required):
- **Pharmacies**: Medical stores, drug stores, chemists
- **Diagnostic Centers**: Labs, hospitals, imaging centers
- **Specialized Centers**: CT scan, MRI, X-ray facilities

### 5. **Rich Service Information**
For each service, displays:
- ✅ **Name** and **Address**
- 📍 **Distance** from patient (in km)
- ⭐ **Rating** (when available)
- 📞 **Phone Number** (click to call)
- 🕒 **Open/Closed Status**
- 🗺️ **Directions** (Google Maps integration)
- 🏥 **Services Offered** (for diagnostic centers)

### 6. **Interactive Map**
- Embedded OpenStreetMap showing all nearby services
- Click on service card to focus on map
- Visual markers for patient location and services
- Direct link to open full map

---

## 🔄 User Flow

### **STEP 1: Doctor Completes Consultation**
```
Doctor → Consultations → Update Consultation
├── Enter Diagnosis
├── Enter Prescription (medicines/tests)
└── Set Status to "Completed"
```

### **STEP 2: Automatic Trigger**
```
System analyzes prescription:
├── Detects medicines → Suggests "Find Medical Stores"
├── Detects tests → Suggests "Find Diagnostic Labs"
└── Detects both → Suggests "Find Both Services"
```

### **STEP 3: Patient Notification**
```
Patient receives notification:
├── Title: "💊 Medicines Prescribed - Find Nearby Stores"
├── Message: "Dr. [Name] has prescribed medicines..."
└── Action: Click to view nearby services
```

### **STEP 4: Location Detection**
```
Patient clicks notification:
├── System requests GPS permission
├── Detects current location (lat, lng)
└── Or patient enters address manually
```

### **STEP 5: Service Search**
```
System searches for services:
├── Queries OpenStreetMap Overpass API
├── Filters by service type (pharmacy/diagnostic)
├── Calculates distances
└── Sorts by proximity
```

### **STEP 6: Results Display**
```
Patient sees:
├── List of top 10-15 nearby services
├── Interactive map with markers
├── Service details (address, phone, distance)
└── Action buttons (Call, Directions)
```

---

## 🛠️ Technical Implementation

### **Backend Routes**

#### 1. `/patient/nearby-services/<consultation_id>`
- Displays nearby services page for a specific consultation
- Analyzes prescription and shows smart suggestions

#### 2. `/api/nearby-services` (POST)
- Fetches nearby pharmacies and diagnostic centers
- **Parameters**:
  - `location`: "lat,lng" or address string
  - `prescription`: Prescription text
  - `service_type`: "pharmacy", "diagnostic", or "all"
- **Returns**: JSON with pharmacies and diagnostic centers

#### 3. `/api/analyze-prescription` (POST)
- Analyzes prescription text
- **Parameters**: `prescription` (text)
- **Returns**: 
  - `service_type`: What services are needed
  - `medicines`: List of extracted medicine names
  - `tests`: List of extracted diagnostic tests
  - `suggestions`: Smart suggestions for patient

### **Helper Functions**

#### `analyze_prescription_type(prescription_text)`
```python
# Analyzes prescription to determine service type
# Returns: 'pharmacy', 'diagnostic', or 'both'
```

#### `extract_medicines(prescription_text)`
```python
# Extracts medicine names from prescription
# Returns: List of medicine names
```

#### `extract_diagnostic_tests(prescription_text)`
```python
# Extracts diagnostic test names
# Returns: List of test names (CT Scan, MRI, Blood Test, etc.)
```

#### `find_nearby_pharmacies(lat, lng, radius=5000)`
```python
# Finds nearby pharmacies using Overpass API
# Returns: List of pharmacy objects with details
```

#### `find_nearby_diagnostic_centers(lat, lng, prescription='', radius=5000)`
```python
# Finds nearby diagnostic centers
# Returns: List of diagnostic center objects
```

#### `calculate_distance(lat1, lng1, lat2, lng2)`
```python
# Calculates distance using Haversine formula
# Returns: Distance in kilometers
```

---

## 📊 Prescription Analysis Keywords

### **Medicines Keywords**
```
tablet, capsule, syrup, injection, mg, ml, dose,
morning, evening, night, before food, after food,
paracetamol, ibuprofen, antibiotic, medicine, medication
```

### **Diagnostic Tests Keywords**
```
CT Scan: ct scan, ct-scan, computed tomography
MRI: mri, magnetic resonance
X-Ray: x-ray, xray, radiography
Ultrasound: ultrasound, sonography, usg
Blood Test: blood test, blood work, cbc, hemoglobin
ECG: ecg, ekg, electrocardiogram
Thyroid: thyroid, tsh, t3, t4
Diabetes: glucose, hba1c, diabetes test
Lipid Profile: lipid profile, cholesterol
Liver Function: liver function, lft, sgpt, sgot
Kidney Function: kidney function, kft, creatinine
```

---

## 🗺️ OpenStreetMap Integration

### **Why OpenStreetMap?**
- ✅ **Free** - No API key required
- ✅ **No Rate Limits** - Unlimited requests
- ✅ **Global Coverage** - Works worldwide
- ✅ **Community-Driven** - Constantly updated
- ✅ **Privacy-Friendly** - No tracking

### **Overpass API Query Example**
```javascript
[out:json][timeout:15];
(
  node["amenity"="pharmacy"](around:5000,12.9716,77.5946);
  way["amenity"="pharmacy"](around:5000,12.9716,77.5946);
);
out body 15;
```

### **Service Tags Used**
- **Pharmacies**: `amenity=pharmacy`
- **Hospitals**: `amenity=hospital`
- **Clinics**: `amenity=clinic`
- **Labs**: `healthcare=laboratory`

---

## 🎨 Frontend Features

### **Smart Suggestions Cards**
```html
<div class="suggestion-card">
  <h5>💊 Buy Prescribed Medicines</h5>
  <p>You have 3 medicine(s) prescribed. Find nearby medical stores.</p>
  <button>Find Medical Stores</button>
</div>
```

### **Service Cards**
```html
<div class="service-card">
  <h5>1. Apollo Pharmacy</h5>
  <p>📍 123 Main Street, Bangalore</p>
  <span class="badge">2.3 km</span>
  <span class="badge">🟢 Open</span>
  <button>📞 Call</button>
  <button>🗺️ Directions</button>
</div>
```

### **Interactive Map**
- Embedded OpenStreetMap iframe
- Shows user location and all nearby services
- Click service card to focus on map
- "Open Full Map" button for detailed navigation

---

## 📱 Mobile Responsiveness

- Fully responsive design
- Touch-friendly buttons
- GPS location detection on mobile
- Click-to-call phone numbers
- One-tap directions to Google Maps

---

## 🔒 Privacy & Security

- **Location Permission**: Requested only when needed
- **No Tracking**: OpenStreetMap doesn't track users
- **Secure**: All API calls over HTTPS
- **Patient Data**: Prescription data never sent to external APIs
- **Local Processing**: Prescription analysis done server-side

---

## 🚀 Setup Instructions

### **1. No API Key Required!**
The feature works out-of-the-box using OpenStreetMap's free Overpass API.

### **2. Optional: Google Places API**
For enhanced results (ratings, photos, reviews):
```bash
# Get API key from: https://console.cloud.google.com/apis/credentials
# Add to .env file:
GOOGLE_PLACES_API_KEY=your_api_key_here
```

### **3. Test the Feature**
1. Login as doctor
2. Complete a consultation with prescription
3. Login as patient
4. Check notifications
5. Click "Find Nearby Services"
6. Allow location access
7. View results!

---

## 📈 Future Enhancements

### **Planned Features**
- [ ] **Medicine Availability Check**: Real-time stock checking
- [ ] **Price Comparison**: Compare medicine prices across stores
- [ ] **Online Ordering**: Direct integration with pharmacy delivery
- [ ] **Appointment Booking**: Book diagnostic tests directly
- [ ] **User Reviews**: Patient ratings for services
- [ ] **Insurance Integration**: Check insurance coverage
- [ ] **Multi-Language**: Support for regional languages
- [ ] **Voice Search**: Voice-based location input
- [ ] **Favorites**: Save frequently used pharmacies/labs
- [ ] **History**: Track past service visits

### **Advanced Features**
- [ ] **AI-Powered Recommendations**: ML-based service suggestions
- [ ] **Route Optimization**: Best route for multiple pickups
- [ ] **Real-Time Availability**: Live medicine stock updates
- [ ] **Telemedicine Integration**: Virtual pharmacy consultations
- [ ] **Health Insurance Claims**: Auto-generate claim forms

---

## 🐛 Troubleshooting

### **Issue: Location not detected**
**Solution**: 
- Check browser location permissions
- Try manual address input
- Use pincode instead of full address

### **Issue: No services found**
**Solution**:
- Verify location is correct
- Try expanding search radius
- Check if area has OpenStreetMap coverage
- Search in nearby city

### **Issue: Map not loading**
**Solution**:
- Check internet connection
- Disable ad blockers
- Try different browser
- Clear browser cache

### **Issue: Prescription not analyzed correctly**
**Solution**:
- Use standard medical terminology
- Include dosage information (mg, ml)
- Separate medicines and tests clearly
- Use line breaks between items

---

## 📞 Support

For issues or questions:
- Check console logs for errors
- Verify database has consultation data
- Test with sample prescriptions
- Contact system administrator

---

## 📄 License

This feature is part of the Medical System application.
Uses OpenStreetMap data © OpenStreetMap contributors.

---

## 🙏 Credits

- **OpenStreetMap**: Free map data and Overpass API
- **Leaflet.js**: Interactive maps (optional)
- **Bootstrap**: UI components
- **Font Awesome**: Icons

---

**Last Updated**: April 30, 2026
**Version**: 1.0.0
**Status**: ✅ Production Ready
