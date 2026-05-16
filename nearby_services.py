"""
Nearby Medical Services Finder
Finds pharmacies, MRI centers, and CT scan centers near user location
"""

import requests
import math
from typing import List, Dict, Tuple, Optional
import json

class NearbyMedicalServices:
    def __init__(self):
        # Google Places API key (you'll need to add your own)
        import os
        self.google_api_key = os.environ.get('GOOGLE_PLACES_API_KEY', 'YOUR_GOOGLE_PLACES_API_KEY')
        self.radius = 10000  # 10 km in meters
        self.max_radius = 25000  # 25 km for expanded search
        
    def get_coordinates_from_pincode(self, pincode: str) -> Optional[Tuple[float, float]]:
        """
        Convert pincode to latitude and longitude
        """
        try:
            # Using OpenStreetMap Nominatim API (free)
            url = f"https://nominatim.openstreetmap.org/search?postalcode={pincode}&country=India&format=json"
            headers = {'User-Agent': 'MediConnect/1.0'}
            response = requests.get(url, headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                if data:
                    return (float(data[0]['lat']), float(data[0]['lon']))
            return None
        except Exception as e:
            print(f"Error getting coordinates: {e}")
            return None
    
    def calculate_distance(self, lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """
        Calculate distance between two coordinates using Haversine formula
        Returns distance in kilometers
        """
        R = 6371  # Earth's radius in kilometers
        
        lat1_rad = math.radians(lat1)
        lat2_rad = math.radians(lat2)
        delta_lat = math.radians(lat2 - lat1)
        delta_lon = math.radians(lon2 - lon1)
        
        a = math.sin(delta_lat/2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(delta_lon/2)**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
        
        distance = R * c
        return round(distance, 2)
    
    def find_nearby_pharmacies(self, latitude: float, longitude: float) -> List[Dict]:
        """
        Find nearby pharmacies using Google Places API
        """
        try:
            url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
            params = {
                'location': f"{latitude},{longitude}",
                'radius': self.radius,
                'type': 'pharmacy',
                'key': self.google_api_key
            }
            
            response = requests.get(url, params=params)
            
            if response.status_code == 200:
                data = response.json()
                pharmacies = []
                
                for place in data.get('results', []):
                    pharmacy = {
                        'name': place.get('name'),
                        'address': place.get('vicinity'),
                        'latitude': place['geometry']['location']['lat'],
                        'longitude': place['geometry']['location']['lng'],
                        'rating': place.get('rating', 'N/A'),
                        'open_now': place.get('opening_hours', {}).get('open_now', 'Unknown'),
                        'place_id': place.get('place_id')
                    }
                    
                    # Calculate distance
                    pharmacy['distance'] = self.calculate_distance(
                        latitude, longitude,
                        pharmacy['latitude'], pharmacy['longitude']
                    )
                    
                    pharmacies.append(pharmacy)
                
                # Sort by distance
                pharmacies.sort(key=lambda x: x['distance'])
                return pharmacies
            
            return []
        except Exception as e:
            print(f"Error finding pharmacies: {e}")
            return []
    
    def find_diagnostic_centers(self, latitude: float, longitude: float, service_type: str = 'all') -> List[Dict]:
        """
        Find nearby MRI and CT scan centers
        service_type: 'mri', 'ct', or 'all'
        """
        try:
            # Search for diagnostic centers, radiology centers, imaging centers
            search_terms = ['diagnostic center', 'radiology center', 'imaging center', 'scan center']
            all_centers = []
            
            for term in search_terms:
                url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
                params = {
                    'location': f"{latitude},{longitude}",
                    'radius': self.radius,
                    'keyword': term,
                    'key': self.google_api_key
                }
                
                response = requests.get(url, params=params)
                
                if response.status_code == 200:
                    data = response.json()
                    
                    for place in data.get('results', []):
                        center = {
                            'name': place.get('name'),
                            'address': place.get('vicinity'),
                            'latitude': place['geometry']['location']['lat'],
                            'longitude': place['geometry']['location']['lng'],
                            'rating': place.get('rating', 'N/A'),
                            'open_now': place.get('opening_hours', {}).get('open_now', 'Unknown'),
                            'place_id': place.get('place_id'),
                            'services': []
                        }
                        
                        # Detect services from name
                        name_lower = place.get('name', '').lower()
                        if 'mri' in name_lower or 'magnetic' in name_lower:
                            center['services'].append('MRI')
                        if 'ct' in name_lower or 'computed tomography' in name_lower:
                            center['services'].append('CT Scan')
                        if not center['services']:
                            center['services'] = ['MRI', 'CT Scan']  # Assume both if not specified
                        
                        # Calculate distance
                        center['distance'] = self.calculate_distance(
                            latitude, longitude,
                            center['latitude'], center['longitude']
                        )
                        
                        all_centers.append(center)
            
            # Remove duplicates based on place_id
            unique_centers = {center['place_id']: center for center in all_centers}.values()
            centers_list = list(unique_centers)
            
            # Filter by service type if specified
            if service_type == 'mri':
                centers_list = [c for c in centers_list if 'MRI' in c['services']]
            elif service_type == 'ct':
                centers_list = [c for c in centers_list if 'CT Scan' in c['services']]
            
            # Sort by distance
            centers_list.sort(key=lambda x: x['distance'])
            return centers_list
        
        except Exception as e:
            print(f"Error finding diagnostic centers: {e}")
            return []
    
    def get_place_details(self, place_id: str) -> Dict:
        """
        Get detailed information about a place including phone number
        """
        try:
            url = "https://maps.googleapis.com/maps/api/place/details/json"
            params = {
                'place_id': place_id,
                'fields': 'name,formatted_phone_number,website,opening_hours',
                'key': self.google_api_key
            }
            
            response = requests.get(url, params=params)
            
            if response.status_code == 200:
                data = response.json()
                result = data.get('result', {})
                return {
                    'phone': result.get('formatted_phone_number', 'N/A'),
                    'website': result.get('website', 'N/A'),
                    'hours': result.get('opening_hours', {}).get('weekday_text', [])
                }
            
            return {}
        except Exception as e:
            print(f"Error getting place details: {e}")
            return {}
    
    def extract_medicines_from_prescription(self, prescription_text: str) -> List[str]:
        """
        Extract medicine names from prescription text
        Simple implementation - can be enhanced with NLP
        """
        # Common medicine name patterns
        medicines = []
        lines = prescription_text.split('\n')
        
        for line in lines:
            line = line.strip()
            # Skip empty lines and common non-medicine words
            if line and len(line) > 3:
                # Remove dosage information
                medicine = line.split('-')[0].split('(')[0].strip()
                if medicine:
                    medicines.append(medicine)
        
        return medicines
    
    def check_medicine_availability(self, pharmacy_place_id: str, medicine_name: str) -> bool:
        """
        Check if medicine is available at pharmacy
        Note: This requires pharmacy API integration (not commonly available)
        Returns True as placeholder
        """
        # This would require integration with pharmacy inventory systems
        # Most pharmacies don't have public APIs for this
        return True  # Placeholder
    
    def suggest_alternatives(self, latitude: float, longitude: float, service_type: str) -> List[Dict]:
        """
        Suggest alternatives if no results found nearby
        Expand search radius or suggest nearby cities
        """
        # Expand search radius to 25 km
        expanded_radius = 25000
        
        if service_type == 'pharmacy':
            return self.find_nearby_pharmacies(latitude, longitude)
        else:
            return self.find_diagnostic_centers(latitude, longitude, service_type)
    
    def format_results(self, pharmacies: List[Dict], diagnostic_centers: List[Dict]) -> Dict:
        """
        Format results in structured output
        """
        return {
            'pharmacies': [
                {
                    'name': p['name'],
                    'address': p['address'],
                    'distance_km': p['distance'],
                    'rating': p['rating'],
                    'open_now': p['open_now'],
                    'coordinates': {
                        'latitude': p['latitude'],
                        'longitude': p['longitude']
                    },
                    'services': ['Medicines']
                }
                for p in pharmacies[:10]  # Top 10 results
            ],
            'diagnostic_centers': [
                {
                    'name': c['name'],
                    'address': c['address'],
                    'distance_km': c['distance'],
                    'rating': c['rating'],
                    'open_now': c['open_now'],
                    'coordinates': {
                        'latitude': c['latitude'],
                        'longitude': c['longitude']
                    },
                    'services': c['services']
                }
                for c in diagnostic_centers[:10]  # Top 10 results
            ]
        }
    
    def search_nearby_services(self, location_input: str, prescription_text: str = None, 
                               search_type: str = 'all') -> Dict:
        """
        Main function to search for nearby medical services
        
        Args:
            location_input: Either "lat,lon" or pincode
            prescription_text: Text of prescription (optional)
            search_type: 'pharmacy', 'mri', 'ct', or 'all'
        
        Returns:
            Dictionary with pharmacies and diagnostic centers
        """
        # Parse location
        if ',' in location_input:
            # Latitude, Longitude format
            lat, lon = map(float, location_input.split(','))
        else:
            # Pincode format
            coords = self.get_coordinates_from_pincode(location_input)
            if not coords:
                return {'error': 'Invalid pincode or location not found'}
            lat, lon = coords
        
        # Extract medicines if prescription provided
        medicines = []
        if prescription_text:
            medicines = self.extract_medicines_from_prescription(prescription_text)
        
        # Search for services
        pharmacies = []
        diagnostic_centers = []
        
        if search_type in ['pharmacy', 'all']:
            pharmacies = self.find_nearby_pharmacies(lat, lon)
            if not pharmacies:
                pharmacies = self.suggest_alternatives(lat, lon, 'pharmacy')
        
        if search_type in ['mri', 'ct', 'all']:
            service = 'all' if search_type == 'all' else search_type
            diagnostic_centers = self.find_diagnostic_centers(lat, lon, service)
            if not diagnostic_centers:
                diagnostic_centers = self.suggest_alternatives(lat, lon, service)
        
        # Format and return results
        results = self.format_results(pharmacies, diagnostic_centers)
        results['medicines_extracted'] = medicines
        results['search_location'] = {'latitude': lat, 'longitude': lon}
        
        return results


# Example usage
if __name__ == "__main__":
    service = NearbyMedicalServices()
    
    # Example 1: Search by pincode
    print("Searching near pincode 560001 (Bangalore)...")
    results = service.search_nearby_services("560001", search_type='all')
    print(json.dumps(results, indent=2))
    
    # Example 2: Search by coordinates
    print("\nSearching near coordinates 12.9716,77.5946 (Bangalore)...")
    results = service.search_nearby_services("12.9716,77.5946", search_type='pharmacy')
    print(json.dumps(results, indent=2))
    
    # Example 3: With prescription
    prescription = """
    Paracetamol 500mg - 1-0-1
    Amoxicillin 250mg - 1-1-1
    Vitamin D3 - 0-0-1
    """
    results = service.search_nearby_services("560001", prescription_text=prescription)
    print(f"\nMedicines extracted: {results['medicines_extracted']}")
