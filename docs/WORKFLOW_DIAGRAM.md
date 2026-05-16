# 🔄 Nearby Medical Services - Workflow Diagram

## Complete System Flow

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    INTELLIGENT HEALTHCARE ASSISTANT                      │
│                   Nearby Medical Services Feature                        │
└─────────────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────────────┐
│ STEP 1: DOCTOR COMPLETES CONSULTATION                                    │
└──────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
                    ┌───────────────────────────┐
                    │   Doctor Dashboard        │
                    │   ├─ View Consultations   │
                    │   ├─ Select Patient       │
                    │   └─ Update Consultation  │
                    └───────────────────────────┘
                                    │
                                    ▼
                    ┌───────────────────────────┐
                    │   Enter Details:          │
                    │   ├─ Diagnosis            │
                    │   ├─ Prescription         │
                    │   │   ├─ Medicines        │
                    │   │   └─ Tests            │
                    │   └─ Status: Completed    │
                    └───────────────────────────┘
                                    │
                                    ▼
┌──────────────────────────────────────────────────────────────────────────┐
│ STEP 2: AUTOMATIC PRESCRIPTION ANALYSIS                                  │
└──────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
                    ┌───────────────────────────┐
                    │  analyze_prescription()   │
                    │  ├─ Scan for keywords     │
                    │  ├─ Detect medicines      │
                    │  └─ Detect tests          │
                    └───────────────────────────┘
                                    │
                    ┌───────────────┴───────────────┐
                    │                               │
                    ▼                               ▼
        ┌─────────────────────┐       ┌─────────────────────┐
        │  Medicine Keywords  │       │  Test Keywords      │
        │  ├─ tablet          │       │  ├─ ct scan         │
        │  ├─ capsule         │       │  ├─ mri             │
        │  ├─ syrup           │       │  ├─ x-ray           │
        │  ├─ injection       │       │  ├─ blood test      │
        │  ├─ mg, ml          │       │  ├─ ultrasound      │
        │  └─ paracetamol     │       │  └─ ecg             │
        └─────────────────────┘       └─────────────────────┘
                    │                               │
                    └───────────────┬───────────────┘
                                    ▼
                    ┌───────────────────────────┐
                    │  Determine Service Type:  │
                    │  ├─ pharmacy              │
                    │  ├─ diagnostic            │
                    │  └─ both                  │
                    └───────────────────────────┘
                                    │
                                    ▼
┌──────────────────────────────────────────────────────────────────────────┐
│ STEP 3: SMART NOTIFICATION GENERATION                                    │
└──────────────────────────────────────────────────────────────────────────┘
                                    │
                    ┌───────────────┴───────────────┐
                    │                               │
                    ▼                               ▼
        ┌─────────────────────┐       ┌─────────────────────┐
        │  If: pharmacy       │       │  If: diagnostic     │
        │  ├─ Title:          │       │  ├─ Title:          │
        │  │   "💊 Medicines  │       │  │   "🔬 Tests      │
        │  │   Prescribed"    │       │  │   Recommended"   │
        │  └─ Message:        │       │  └─ Message:        │
        │      "Find nearby   │       │      "Find nearby   │
        │      medical stores"│       │      diagnostic labs"│
        └─────────────────────┘       └─────────────────────┘
                    │                               │
                    └───────────────┬───────────────┘
                                    ▼
                    ┌───────────────────────────┐
                    │  Create Notification:     │
                    │  ├─ user_id: patient      │
                    │  ├─ title: Smart title    │
                    │  ├─ message: Smart msg    │
                    │  └─ type: prescription    │
                    └───────────────────────────┘
                                    │
                                    ▼
                    ┌───────────────────────────┐
                    │  Insert into Database     │
                    │  notifications table      │
                    └───────────────────────────┘
                                    │
                                    ▼
┌──────────────────────────────────────────────────────────────────────────┐
│ STEP 4: PATIENT RECEIVES NOTIFICATION                                    │
└──────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
                    ┌───────────────────────────┐
                    │  Patient Dashboard        │
                    │  ├─ Notification Badge    │
                    │  ├─ Click Notification    │
                    │  └─ View Details          │
                    └───────────────────────────┘
                                    │
                                    ▼
                    ┌───────────────────────────┐
                    │  Consultation History     │
                    │  ├─ View Prescription     │
                    │  ├─ See Smart Suggestions │
                    │  └─ Click "Find Services" │
                    └───────────────────────────┘
                                    │
                                    ▼
┌──────────────────────────────────────────────────────────────────────────┐
│ STEP 5: LOCATION DETECTION                                               │
└──────────────────────────────────────────────────────────────────────────┘
                                    │
                    ┌───────────────┴───────────────┐
                    │                               │
                    ▼                               ▼
        ┌─────────────────────┐       ┌─────────────────────┐
        │  Option 1: GPS      │       │  Option 2: Manual   │
        │  ├─ Request         │       │  ├─ Enter address   │
        │  │   permission     │       │  ├─ Or pincode      │
        │  ├─ Get coordinates │       │  └─ Geocode to      │
        │  └─ lat, lng        │       │      coordinates    │
        └─────────────────────┘       └─────────────────────┘
                    │                               │
                    └───────────────┬───────────────┘
                                    ▼
                    ┌───────────────────────────┐
                    │  User Location:           │
                    │  ├─ Latitude: 12.9716     │
                    │  └─ Longitude: 77.5946    │
                    └───────────────────────────┘
                                    │
                                    ▼
┌──────────────────────────────────────────────────────────────────────────┐
│ STEP 6: SEARCH NEARBY SERVICES                                           │
└──────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
                    ┌───────────────────────────┐
                    │  API Call:                │
                    │  /api/nearby-services     │
                    │  ├─ location: lat,lng     │
                    │  ├─ prescription: text    │
                    │  └─ service_type: all     │
                    └───────────────────────────┘
                                    │
                    ┌───────────────┴───────────────┐
                    │                               │
                    ▼                               ▼
        ┌─────────────────────┐       ┌─────────────────────┐
        │  Find Pharmacies    │       │  Find Diagnostic    │
        │  ├─ Query OSM       │       │  ├─ Query OSM       │
        │  ├─ amenity=        │       │  ├─ amenity=        │
        │  │   pharmacy       │       │  │   hospital       │
        │  ├─ radius: 5km     │       │  ├─ amenity=clinic  │
        │  └─ Get results     │       │  └─ healthcare=lab  │
        └─────────────────────┘       └─────────────────────┘
                    │                               │
                    └───────────────┬───────────────┘
                                    ▼
                    ┌───────────────────────────┐
                    │  OpenStreetMap            │
                    │  Overpass API             │
                    │  ├─ Free service          │
                    │  ├─ No API key            │
                    │  └─ Global coverage       │
                    └───────────────────────────┘
                                    │
                                    ▼
                    ┌───────────────────────────┐
                    │  Process Results:         │
                    │  ├─ Extract data          │
                    │  ├─ Calculate distances   │
                    │  ├─ Sort by proximity     │
                    │  └─ Format response       │
                    └───────────────────────────┘
                                    │
                                    ▼
┌──────────────────────────────────────────────────────────────────────────┐
│ STEP 7: DISPLAY RESULTS                                                  │
└──────────────────────────────────────────────────────────────────────────┘
                                    │
                    ┌───────────────┴───────────────┐
                    │                               │
                    ▼                               ▼
        ┌─────────────────────┐       ┌─────────────────────┐
        │  Service List       │       │  Interactive Map    │
        │  ├─ Name            │       │  ├─ User marker     │
        │  ├─ Address         │       │  ├─ Service markers │
        │  ├─ Distance        │       │  ├─ Click to focus  │
        │  ├─ Phone           │       │  └─ Zoom controls   │
        │  ├─ Rating          │       └─────────────────────┘
        │  └─ Open/Closed     │
        └─────────────────────┘
                    │
                    ▼
        ┌─────────────────────┐
        │  Action Buttons:    │
        │  ├─ 📞 Call         │
        │  ├─ 🗺️ Directions  │
        │  └─ 💾 Save         │
        └─────────────────────┘
                    │
                    ▼
┌──────────────────────────────────────────────────────────────────────────┐
│ STEP 8: PATIENT ACTIONS                                                  │
└──────────────────────────────────────────────────────────────────────────┘
                                    │
                    ┌───────────────┴───────────────┐
                    │                               │
                    ▼                               ▼
        ┌─────────────────────┐       ┌─────────────────────┐
        │  Call Pharmacy      │       │  Get Directions     │
        │  ├─ Click phone     │       │  ├─ Open Google Maps│
        │  ├─ Direct dial     │       │  ├─ Route from      │
        │  └─ Inquire stock   │       │  │   current loc    │
        └─────────────────────┘       │  └─ Navigate        │
                                      └─────────────────────┘
                    │                               │
                    └───────────────┬───────────────┘
                                    ▼
                    ┌───────────────────────────┐
                    │  Patient Visits Service   │
                    │  ├─ Buy medicines         │
                    │  ├─ Book diagnostic test  │
                    │  └─ Complete treatment    │
                    └───────────────────────────┘
                                    │
                                    ▼
                    ┌───────────────────────────┐
                    │  ✅ TREATMENT COMPLETE    │
                    └───────────────────────────┘

═══════════════════════════════════════════════════════════════════════════

                        KEY TECHNOLOGIES USED

┌─────────────────────────────────────────────────────────────────────────┐
│                                                                          │
│  Backend:                                                                │
│  ├─ Flask (Python) - Web framework                                      │
│  ├─ SQLite - Database                                                   │
│  ├─ Requests - HTTP client                                              │
│  └─ Math - Distance calculations                                        │
│                                                                          │
│  Frontend:                                                               │
│  ├─ Bootstrap 5 - UI framework                                          │
│  ├─ JavaScript - Interactivity                                          │
│  ├─ HTML5 Geolocation API - GPS                                         │
│  └─ Font Awesome - Icons                                                │
│                                                                          │
│  External APIs:                                                          │
│  ├─ OpenStreetMap Overpass API - Service search (FREE)                  │
│  ├─ OpenStreetMap Nominatim - Geocoding (FREE)                          │
│  └─ Google Maps - Directions (FREE)                                     │
│                                                                          │
│  Optional:                                                               │
│  └─ Google Places API - Enhanced data (ratings, reviews)                │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘

═══════════════════════════════════════════════════════════════════════════

                        DATA FLOW SUMMARY

┌─────────────────────────────────────────────────────────────────────────┐
│                                                                          │
│  1. Doctor → Prescription → Database                                    │
│  2. Database → Analysis → Service Type                                  │
│  3. Service Type → Notification → Patient                               │
│  4. Patient → Location → API Request                                    │
│  5. API Request → OpenStreetMap → Results                               │
│  6. Results → Processing → Display                                      │
│  7. Display → Patient Action → Service Visit                            │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘

═══════════════════════════════════════════════════════════════════════════

                        SECURITY & PRIVACY

┌─────────────────────────────────────────────────────────────────────────┐
│                                                                          │
│  ✅ Location permission requested only when needed                      │
│  ✅ Prescription data never sent to external APIs                       │
│  ✅ All analysis done server-side                                       │
│  ✅ No tracking by OpenStreetMap                                        │
│  ✅ HTTPS for all API calls                                             │
│  ✅ Patient data encrypted in database                                  │
│  ✅ Session-based authentication                                        │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘

═══════════════════════════════════════════════════════════════════════════
```

## Quick Reference

### Prescription Keywords Detected

**Medicines:**
- tablet, capsule, syrup, injection
- mg, ml, dose
- morning, evening, night
- before food, after food
- Common drug names

**Diagnostic Tests:**
- CT scan, MRI, X-ray
- Blood test, urine test
- Ultrasound, ECG
- Lab tests (CBC, LFT, KFT)
- Imaging tests

### Service Types Returned

1. **pharmacy** - Only medicines prescribed
2. **diagnostic** - Only tests recommended
3. **both** - Medicines and tests prescribed

### Distance Calculation

Uses **Haversine Formula**:
```
distance = 2 * R * arcsin(√(sin²(Δlat/2) + cos(lat1) * cos(lat2) * sin²(Δlon/2)))
where R = 6371 km (Earth's radius)
```

### API Endpoints

- `GET /patient/nearby-services/<consultation_id>` - View page
- `POST /api/nearby-services` - Search services
- `POST /api/analyze-prescription` - Analyze prescription

---

**Last Updated**: April 30, 2026  
**Version**: 1.0.0
