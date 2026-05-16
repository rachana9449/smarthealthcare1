#!/usr/bin/env python3
"""
Test script to verify dashboard routes work with both slash and hyphen formats
"""

import requests
import sys

def test_routes():
    base_url = "http://127.0.0.1:5000"
    
    # Test routes (these should redirect to login if not authenticated)
    routes_to_test = [
        # Original slash routes
        "/doctor/dashboard",
        "/patient/dashboard", 
        "/admin/dashboard",
        
        # New hyphen routes
        "/doctor-dashboard",
        "/patient-dashboard",
        "/admin-dashboard"
    ]
    
    print("🧪 Testing Dashboard Routes...")
    print("=" * 50)
    
    for route in routes_to_test:
        try:
            url = f"{base_url}{route}"
            response = requests.get(url, allow_redirects=False, timeout=5)
            
            if response.status_code == 302:
                # Redirect is expected for protected routes
                redirect_location = response.headers.get('Location', 'Unknown')
                print(f"✅ {route:<20} → {response.status_code} (Redirect to: {redirect_location})")
            elif response.status_code == 404:
                print(f"❌ {route:<20} → {response.status_code} (Not Found)")
            else:
                print(f"ℹ️  {route:<20} → {response.status_code}")
                
        except requests.exceptions.RequestException as e:
            print(f"❌ {route:<20} → Error: {e}")
    
    print("\n" + "=" * 50)
    print("📋 Test Summary:")
    print("✅ = Route exists (redirects to login as expected)")
    print("❌ = Route not found (404 error)")
    print("ℹ️  = Other response")
    
    print(f"\n🌐 Flask app should be running at: {base_url}")
    print("🔐 Remember: You need to login first to access dashboards!")

if __name__ == "__main__":
    test_routes()