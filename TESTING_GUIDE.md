# 🧪 Testing Guide - Healthcare Application Enhancements

## Quick Start Testing

### Prerequisites
```bash
# Ensure all dependencies are installed
pip install -r requirements.txt

# Start the application
python app.py
```

The application will run on: `http://localhost:5000`

---

## 🎯 Test Scenarios

### 1. Voice Input Feature (5 minutes)

**Steps:**
1. Open browser and go to `http://localhost:5000`
2. Login as Patient (or create new patient account)
3. Click "Check Symptoms" from dashboard
4. Look for the green microphone button next to the textarea
5. Click the microphone button
6. **Allow microphone access** when browser prompts
7. Speak clearly: "I have fever, headache, body ache, and cough for three days"
8. Click the red stop button
9. Verify text appears in the textarea

**Expected Result:**
- ✅ Button turns red and animates while listening
- ✅ Toast notification shows "Listening..."
- ✅ Spoken words appear as text
- ✅ Character count updates automatically

**Troubleshooting:**
- If microphone doesn't work, check browser permissions
- Chrome/Edge work best for voice input
- Firefox may require additional permissions

---

### 2. Delete Consultation History (3 minutes)

**Steps:**
1. Login as Patient
2. Navigate to "Consultation History"
3. If no consultations exist, create one first:
   - Go to "Consult Doctor"
   - Select any doctor
   - Submit symptoms
4. Back to "Consultation History"
5. Click the red "Delete" button next to any consultation
6. Read the confirmation popup
7. Click "Yes, Delete It"

**Expected Result:**
- ✅ Beautiful SweetAlert2 popup appears
- ✅ Warning message explains action is permanent
- ✅ After confirmation, loading spinner shows
- ✅ Success message appears
- ✅ Page refreshes and consultation is gone
- ✅ Related feedback is also deleted

**Test as Doctor:**
1. Login as Doctor
2. Go to "Consultations"
3. Click delete on any consultation
4. Same behavior as patient

---

### 3. Doctor Recommendations (5 minutes)

**Steps:**
1. Login as Patient
2. Go to "Check Symptoms"
3. Enter symptoms: "I have high fever, severe headache, chest pain, and difficulty breathing"
4. Click "Analyze Symptoms"
5. Wait for prediction result
6. Scroll down to see "Recommended Doctors" section

**Expected Result:**
- ✅ Section appears automatically after 1 second
- ✅ Shows recommended specialization (e.g., "Pulmonologist")
- ✅ Displays up to 6 doctors with:
  - Name and specialization
  - Rating (stars)
  - Experience years
  - Consultation fee
  - "Consult Now" button
  - "Book Appointment" button
- ✅ Clicking "Consult Now" goes to consultation page
- ✅ Clicking "Book Appointment" goes to booking page

**Test Different Diseases:**
- "diabetes symptoms" → Should recommend Endocrinologist
- "heart pain chest discomfort" → Should recommend Cardiologist
- "skin rash itching" → Should recommend Dermatologist
- "stomach pain nausea" → Should recommend Gastroenterologist

---

### 4. Real-time Notifications (10 minutes)

**Setup:**
1. Open TWO browser windows (or use incognito mode)
2. Window 1: Login as Doctor
3. Window 2: Login as Patient

**Steps:**
1. **Window 1 (Doctor):**
   - Go to Doctor Dashboard
   - Keep this window visible
   - Watch the top-right corner

2. **Window 2 (Patient):**
   - Go to "Consult Doctor"
   - Select the doctor you're logged in as (Window 1)
   - Click "Book Appointment"
   - Fill in appointment details
   - Submit

3. **Window 1 (Doctor):**
   - Watch for instant notification!

**Expected Result:**
- ✅ Slide-in notification card appears in top-right
- ✅ Beep sound plays
- ✅ Shows patient name, date, time
- ✅ Emergency appointments show red theme
- ✅ Browser desktop notification (if permitted)
- ✅ Notification badge updates in navbar
- ✅ Card auto-dismisses after 15 seconds

**Test Emergency Appointment:**
1. When booking appointment, check "Emergency" checkbox
2. Doctor should see red-themed notification with 🚨 emoji
3. Email notification sent to doctor (if configured)

---

### 5. SweetAlert2 Popups (3 minutes)

**Test Success Popup:**
1. Login as Patient
2. Book an appointment
3. See beautiful success popup

**Test Error Popup:**
1. Try to access a page without logging in
2. See error popup

**Test Confirmation:**
1. Try to delete a consultation
2. See confirmation dialog

**Test Toast Notifications:**
1. Add a symptom badge on symptom checker page
2. See toast notification in top-right

**Expected Result:**
- ✅ All popups are styled beautifully
- ✅ Icons animate
- ✅ Buttons have gradient colors
- ✅ Toast slides in from right
- ✅ Progress bars show timing

---

### 6. Visual Enhancements (5 minutes)

**Test Animations:**
1. Navigate to any dashboard
2. Watch cards fade in
3. Hover over cards - they should lift up
4. Hover over buttons - they should scale

**Test Dark Mode:**
1. Look for theme toggle in navbar (moon/sun icon)
2. Click to switch between light/dark
3. Verify all pages adapt to theme
4. Refresh page - theme should persist

**Test Responsive Design:**
1. Open browser DevTools (F12)
2. Click device toolbar (Ctrl+Shift+M)
3. Test different screen sizes:
   - iPhone SE (375px)
   - iPad (768px)
   - Desktop (1920px)
4. Verify layout adapts properly

**Expected Result:**
- ✅ Smooth fade-in animations
- ✅ Hover effects work
- ✅ Dark mode changes all colors
- ✅ Mobile layout stacks vertically
- ✅ Tablet shows 2-column grid
- ✅ Desktop shows full layout

---

### 7. Nearby Services (5 minutes)

**Steps:**
1. Login as Patient
2. Go to "Consultation History"
3. View a completed consultation with prescription
4. Click "Find Medical Store" button
5. **Allow location access** when prompted
6. Wait for results

**Expected Result:**
- ✅ Modal opens with map
- ✅ Location detected automatically
- ✅ List of nearby pharmacies appears
- ✅ OpenStreetMap shows locations
- ✅ Click on result to focus map
- ✅ "Get Directions" link works

**Test Different Service Types:**
- Find Medical Store (pharmacies)
- Find Diagnostic Lab (labs)
- Find CT/MRI Center (imaging centers)

---

## 🔍 Browser Compatibility Testing

### Recommended Browsers:
- ✅ **Chrome 90+** (Best experience)
- ✅ **Edge 90+** (Best experience)
- ✅ **Firefox 88+** (Good, voice input may vary)
- ✅ **Safari 14+** (Good, some features limited)

### Features by Browser:

| Feature | Chrome | Edge | Firefox | Safari |
|---------|--------|------|---------|--------|
| Voice Input | ✅ | ✅ | ⚠️ | ⚠️ |
| Real-time Notifications | ✅ | ✅ | ✅ | ✅ |
| SweetAlert2 | ✅ | ✅ | ✅ | ✅ |
| Geolocation | ✅ | ✅ | ✅ | ✅ |
| Dark Mode | ✅ | ✅ | ✅ | ✅ |

⚠️ = May require additional permissions or have limited support

---

## 🐛 Common Issues & Solutions

### Issue 1: Voice Input Not Working
**Solution:**
```
1. Check browser console for errors
2. Verify microphone permission granted
3. Try Chrome/Edge instead of Firefox
4. Check if HTTPS is enabled (required for production)
5. Test microphone in other apps
```

### Issue 2: Notifications Not Appearing
**Solution:**
```
1. Check if browser blocks notifications
2. Verify doctor is logged in
3. Check browser console for SSE errors
4. Try refreshing doctor dashboard
5. Check if firewall blocks SSE
```

### Issue 3: Delete Not Working
**Solution:**
```
1. Check browser console for errors
2. Verify user is logged in
3. Check if consultation belongs to user
4. Try hard refresh (Ctrl+F5)
5. Check database permissions
```

### Issue 4: Doctor Recommendations Not Showing
**Solution:**
```
1. Verify doctors exist in database
2. Check if doctors have specializations set
3. Run: python create_sample_data.py
4. Check browser console for API errors
5. Verify /api/recommend-doctors route works
```

### Issue 5: Nearby Services Not Loading
**Solution:**
```
1. Allow location permission
2. Check internet connection
3. Verify OpenStreetMap is accessible
4. Try different location
5. Check browser console for errors
```

---

## 📊 Performance Testing

### Load Time Expectations:
- **Dashboard Load:** < 2 seconds
- **Symptom Analysis:** < 3 seconds
- **Doctor Recommendations:** < 1 second
- **Delete Operation:** < 1 second
- **Nearby Services:** < 5 seconds (depends on location)

### Test with Chrome DevTools:
1. Open DevTools (F12)
2. Go to "Network" tab
3. Reload page
4. Check "Load" time at bottom
5. Should be under 2 seconds

---

## 🎯 Acceptance Criteria

### Voice Input:
- [ ] Microphone button visible
- [ ] Permission prompt appears
- [ ] Voice converts to text accurately
- [ ] Button animates while listening
- [ ] Works in Chrome/Edge

### Delete Consultation:
- [ ] Delete button visible
- [ ] Confirmation popup appears
- [ ] Record deleted successfully
- [ ] Page refreshes automatically
- [ ] Related data cleaned up

### Doctor Recommendations:
- [ ] Section appears after prediction
- [ ] Shows relevant specialization
- [ ] Displays doctor cards
- [ ] Buttons navigate correctly
- [ ] Ratings and fees shown

### Real-time Notifications:
- [ ] Notification appears instantly
- [ ] Sound plays
- [ ] Card shows correct info
- [ ] Auto-dismisses after 15s
- [ ] Badge updates

### Visual Enhancements:
- [ ] Animations smooth
- [ ] Dark mode works
- [ ] Responsive on mobile
- [ ] Hover effects work
- [ ] Loading spinners show

---

## 📝 Test Report Template

```markdown
## Test Report - [Date]

### Tester: [Your Name]
### Browser: [Chrome/Edge/Firefox/Safari]
### OS: [Windows/Mac/Linux]

### Test Results:

#### Voice Input: ✅ / ❌
- Notes: 

#### Delete Consultation: ✅ / ❌
- Notes:

#### Doctor Recommendations: ✅ / ❌
- Notes:

#### Real-time Notifications: ✅ / ❌
- Notes:

#### Visual Enhancements: ✅ / ❌
- Notes:

### Issues Found:
1. 
2. 
3. 

### Overall Rating: [1-10]

### Recommendations:
-
-
```

---

## 🚀 Production Checklist

Before deploying to production:

- [ ] All tests pass
- [ ] No console errors
- [ ] HTTPS enabled (required for voice input)
- [ ] Email notifications configured
- [ ] Database backed up
- [ ] Environment variables set
- [ ] Error logging enabled
- [ ] Performance optimized
- [ ] Security headers added
- [ ] CORS configured properly

---

## 📞 Need Help?

If you encounter issues:

1. **Check Console:** Press F12 and look for errors
2. **Check Logs:** Look at terminal where app is running
3. **Check Database:** Verify data exists
4. **Check Permissions:** Browser, microphone, location
5. **Try Different Browser:** Chrome works best

---

**Happy Testing!** 🎉

Remember: All existing functionality is preserved. These are pure enhancements!
