"""
Google Maps and Places API Utilities
Handles location-based services for finding events, universities, and study spots
"""

import os
import requests
from typing import Dict, List, Any

class MapsService:
    def __init__(self):
        self.api_key = os.getenv('GOOGLE_MAPS_API_KEY')
        self.places_base_url = "https://maps.googleapis.com/maps/api/place"
        self.geocoding_base_url = "https://maps.googleapis.com/maps/api/geocode"
        self.directions_base_url = "https://maps.googleapis.com/maps/api/directions"
    
    def find_educational_events(self, location: str, radius: int, event_type: str) -> Dict[str, Any]:
        """Find educational events near a location"""
        try:
            if not self.api_key:
                return self._get_mock_events(location, event_type)
            
            # First, geocode the location
            coords = self._geocode_location(location)
            if not coords:
                return self._get_mock_events(location, event_type)
            
            # Search for venues that commonly host educational events
            venue_types = ['university', 'library', 'community_center', 'convention_center']
            venues = []
            
            for venue_type in venue_types:
                venue_results = self._search_places(
                    location=f"{coords['lat']},{coords['lng']}",
                    radius=radius * 1000,  # Convert km to meters
                    place_type=venue_type
                )
                venues.extend(venue_results.get('results', []))
            
            # Convert venues to mock events (in real implementation, would integrate with event APIs)
            events = self._venues_to_events(venues, event_type)
            
            return {
                'success': True,
                'events': events,
                'search_location': location,
                'coordinates': coords
            }
            
        except Exception as e:
            print(f"Maps API error: {e}")
            return self._get_mock_events(location, event_type)
    
    def find_universities(self, location: str, radius: int) -> Dict[str, Any]:
        """Find universities and educational institutions"""
        try:
            if not self.api_key:
                return self._get_mock_universities(location)
            
            coords = self._geocode_location(location)
            if not coords:
                return self._get_mock_universities(location)
            
            # Search for universities
            university_results = self._search_places(
                location=f"{coords['lat']},{coords['lng']}",
                radius=radius * 1000,
                place_type='university'
            )
            
            # Search for schools as well
            school_results = self._search_places(
                location=f"{coords['lat']},{coords['lng']}",
                radius=radius * 1000,
                place_type='school'
            )
            
            # Combine and format results
            all_institutions = university_results.get('results', []) + school_results.get('results', [])
            universities = self._format_universities(all_institutions)
            
            return {
                'success': True,
                'universities': universities,
                'search_location': location,
                'coordinates': coords
            }
            
        except Exception as e:
            print(f"University search error: {e}")
            return self._get_mock_universities(location)
    
    def find_study_spots(self, location: str, spot_type: str) -> Dict[str, Any]:
        """Find libraries, cafes, and study-friendly locations"""
        try:
            if not self.api_key:
                return self._get_mock_study_spots(location, spot_type)
            
            coords = self._geocode_location(location)
            if not coords:
                return self._get_mock_study_spots(location, spot_type)
            
            # Define search types based on spot_type
            search_types = self._get_study_spot_search_types(spot_type)
            
            all_spots = []
            for search_type in search_types:
                spot_results = self._search_places(
                    location=f"{coords['lat']},{coords['lng']}",
                    radius=10000,  # 10km radius for study spots
                    place_type=search_type
                )
                all_spots.extend(spot_results.get('results', []))
            
            # Format study spots
            formatted_spots = self._format_study_spots(all_spots)
            
            return {
                'success': True,
                'spots': formatted_spots,
                'search_location': location,
                'coordinates': coords
            }
            
        except Exception as e:
            print(f"Study spots search error: {e}")
            return self._get_mock_study_spots(location, spot_type)
    
    def find_networking_events(self, location: str, field: str) -> Dict[str, Any]:
        """Find networking events and meetups"""
        try:
            if not self.api_key:
                return self._get_mock_networking_events(location, field)
            
            coords = self._geocode_location(location)
            if not coords:
                return self._get_mock_networking_events(location, field)
            
            # Search for venues that host networking events
            venue_types = ['convention_center', 'university', 'library', 'restaurant']
            venues = []
            
            for venue_type in venue_types:
                venue_results = self._search_places(
                    location=f"{coords['lat']},{coords['lng']}",
                    radius=25000,  # 25km radius
                    place_type=venue_type
                )
                venues.extend(venue_results.get('results', []))
            
            # Convert venues to networking events
            events = self._venues_to_networking_events(venues, field)
            
            return {
                'success': True,
                'events': events,
                'search_location': location,
                'field': field,
                'coordinates': coords
            }
            
        except Exception as e:
            print(f"Networking events search error: {e}")
            return self._get_mock_networking_events(location, field)
    
    def optimize_multi_destination_route(self, start_location: str, destinations: List[str], travel_mode: str) -> Dict[str, Any]:
        """Optimize route for multiple destinations"""
        try:
            if not self.api_key:
                return self._get_mock_route(start_location, destinations, travel_mode)
            
            # Geocode all locations
            start_coords = self._geocode_location(start_location)
            dest_coords = []
            
            for dest in destinations:
                coords = self._geocode_location(dest)
                if coords:
                    dest_coords.append({'location': dest, 'coords': coords})
            
            if not start_coords or not dest_coords:
                return self._get_mock_route(start_location, destinations, travel_mode)
            
            # Simple route optimization (in real implementation, would use more sophisticated algorithms)
            optimized_order = self._simple_route_optimization(start_coords, dest_coords)
            
            # Calculate route details
            route_details = self._calculate_route_details(start_coords, optimized_order, travel_mode)
            
            return {
                'success': True,
                'route': route_details,
                'start_location': start_location,
                'travel_mode': travel_mode
            }
            
        except Exception as e:
            print(f"Route optimization error: {e}")
            return self._get_mock_route(start_location, destinations, travel_mode)
    
    def _geocode_location(self, location: str) -> Dict[str, float]:
        """Convert location string to coordinates"""
        try:
            url = f"{self.geocoding_base_url}/json"
            params = {
                'address': location,
                'key': self.api_key
            }
            
            response = requests.get(url, params=params)
            data = response.json()
            
            if data['status'] == 'OK' and data['results']:
                location_data = data['results'][0]['geometry']['location']
                return {
                    'lat': location_data['lat'],
                    'lng': location_data['lng']
                }
            
            return None
            
        except Exception as e:
            print(f"Geocoding error: {e}")
            return None
    
    def _search_places(self, location: str, radius: int, place_type: str) -> Dict[str, Any]:
        """Search for places using Google Places API"""
        try:
            url = f"{self.places_base_url}/nearbysearch/json"
            params = {
                'location': location,
                'radius': radius,
                'type': place_type,
                'key': self.api_key
            }
            
            response = requests.get(url, params=params)
            data = response.json()
            
            return data
            
        except Exception as e:
            print(f"Places search error: {e}")
            return {'results': []}
    
    def _get_study_spot_search_types(self, spot_type: str) -> List[str]:
        """Get search types for study spots"""
        type_mapping = {
            'all': ['library', 'cafe', 'university'],
            'libraries': ['library'],
            'cafes': ['cafe', 'restaurant'],
            'coworking': ['library', 'cafe']
        }
        
        return type_mapping.get(spot_type, ['library', 'cafe'])
    
    def _venues_to_events(self, venues: List[Dict], event_type: str) -> List[Dict]:
        """Convert venue data to mock event data"""
        events = []
        import datetime
        import random
        
        event_templates = {
            'hackathons': [
                'CodeFest 2024', 'AI Hackathon', 'Blockchain Challenge', 'Web Dev Marathon'
            ],
            'conferences': [
                'Tech Summit', 'Innovation Conference', 'Developer Days', 'Future of AI'
            ],
            'workshops': [
                'Python Workshop', 'Data Science Bootcamp', 'UI/UX Design Session', 'Coding Fundamentals'
            ]
        }
        
        templates = event_templates.get(event_type, event_templates['workshops'])
        
        for i, venue in enumerate(venues[:10]):  # Limit to 10 events
            event_date = datetime.datetime.now() + datetime.timedelta(days=random.randint(1, 60))
            
            event = {
                'title': random.choice(templates),
                'venue': venue.get('name', 'Unknown Venue'),
                'location': venue.get('vicinity', 'Unknown Location'),
                'date': event_date.strftime('%Y-%m-%d'),
                'time': f"{random.randint(9, 18)}:00",
                'type': event_type,
                'description': f"Educational event at {venue.get('name', 'venue')}",
                'rating': venue.get('rating', 4.0),
                'distance': random.randint(1, 50)  # Mock distance in km
            }
            events.append(event)
        
        return events
    
    def _format_universities(self, institutions: List[Dict]) -> List[Dict]:
        """Format university data"""
        formatted = []
        
        for institution in institutions:
            uni_data = {
                'name': institution.get('name', 'Unknown Institution'),
                'location': institution.get('vicinity', 'Unknown Location'),
                'rating': institution.get('rating', 4.0),
                'user_ratings_total': institution.get('user_ratings_total', 0),
                'place_id': institution.get('place_id', ''),
                'types': institution.get('types', []),
                'geometry': institution.get('geometry', {})
            }
            formatted.append(uni_data)
        
        return formatted
    
    def _format_study_spots(self, spots: List[Dict]) -> List[Dict]:
        """Format study spot data"""
        formatted = []
        
        for spot in spots:
            spot_data = {
                'name': spot.get('name', 'Unknown Location'),
                'location': spot.get('vicinity', 'Unknown Location'),
                'type': self._determine_spot_type(spot.get('types', [])),
                'rating': spot.get('rating', 3.5),
                'user_ratings_total': spot.get('user_ratings_total', 0),
                'price_level': spot.get('price_level', 2),
                'place_id': spot.get('place_id', ''),
                'geometry': spot.get('geometry', {}),
                'opening_hours': spot.get('opening_hours', {})
            }
            formatted.append(spot_data)
        
        return formatted
    
    def _determine_spot_type(self, types: List[str]) -> str:
        """Determine study spot type from Google Places types"""
        if 'library' in types:
            return 'library'
        elif any(t in types for t in ['cafe', 'restaurant', 'food']):
            return 'cafe'
        elif 'university' in types or 'school' in types:
            return 'university'
        else:
            return 'other'
    
    def _venues_to_networking_events(self, venues: List[Dict], field: str) -> List[Dict]:
        """Convert venues to networking events"""
        events = []
        import datetime
        import random
        
        event_templates = {
            'technology': [
                'Tech Professionals Meetup', 'Software Developers Network', 'AI/ML Community', 'Startup Founders Circle'
            ],
            'business': [
                'Business Leaders Forum', 'Entrepreneurship Mixer', 'Young Professionals Network', 'Industry Connect'
            ],
            'science': [
                'Research Network', 'Science & Innovation Meetup', 'STEM Professionals', 'Academic Collaboration'
            ]
        }
        
        templates = event_templates.get(field, event_templates['technology'])
        
        for i, venue in enumerate(venues[:8]):  # Limit to 8 networking events
            event_date = datetime.datetime.now() + datetime.timedelta(days=random.randint(1, 30))
            
            event = {
                'title': random.choice(templates),
                'venue': venue.get('name', 'Unknown Venue'),
                'location': venue.get('vicinity', 'Unknown Location'),
                'date': event_date.strftime('%Y-%m-%d'),
                'time': f"{random.randint(17, 20)}:00",  # Evening events
                'field': field,
                'type': 'networking',
                'description': f"Professional networking event for {field} professionals",
                'attendees_expected': random.randint(20, 100),
                'cost': 'Free' if random.random() > 0.3 else '$10-25'
            }
            events.append(event)
        
        return events
    
    def _simple_route_optimization(self, start: Dict, destinations: List[Dict]) -> List[Dict]:
        """Simple route optimization using nearest neighbor"""
        optimized = []
        current_location = start
        remaining_destinations = destinations.copy()
        
        while remaining_destinations:
            # Find nearest destination
            nearest = min(remaining_destinations, 
                         key=lambda dest: self._calculate_distance(current_location, dest['coords']))
            
            optimized.append(nearest)
            remaining_destinations.remove(nearest)
            current_location = nearest['coords']
        
        return optimized
    
    def _calculate_distance(self, coord1: Dict, coord2: Dict) -> float:
        """Calculate approximate distance between two coordinates"""
        # Simple Euclidean distance (for demo purposes)
        lat_diff = abs(coord1['lat'] - coord2['lat'])
        lng_diff = abs(coord1['lng'] - coord2['lng'])
        return (lat_diff ** 2 + lng_diff ** 2) ** 0.5
    
    def _calculate_route_details(self, start: Dict, destinations: List[Dict], travel_mode: str) -> Dict:
        """Calculate route details"""
        import random
        
        total_distance = sum(random.randint(5, 25) for _ in destinations)  # Mock distances
        
        # Estimate time based on travel mode
        time_multipliers = {
            'driving': 1.0,
            'transit': 1.5,
            'walking': 4.0,
            'bicycling': 2.0
        }
        
        base_time = total_distance * 3  # 3 minutes per km base time
        total_time = int(base_time * time_multipliers.get(travel_mode, 1.0))
        
        return {
            'destinations': [dest['location'] for dest in destinations],
            'optimized_order': destinations,
            'total_distance': total_distance,
            'total_duration': total_time,
            'travel_mode': travel_mode,
            'estimated_cost': self._estimate_travel_cost(total_distance, travel_mode)
        }
    
    def _estimate_travel_cost(self, distance: int, travel_mode: str) -> str:
        """Estimate travel cost"""
        cost_estimates = {
            'driving': f"${distance * 0.5:.0f}-{distance * 0.8:.0f} (fuel + parking)",
            'transit': f"${distance * 0.2:.0f}-{distance * 0.4:.0f} (public transport)",
            'walking': "$0 (free!)",
            'bicycling': f"${distance * 0.1:.0f}-{distance * 0.2:.0f} (bike rental if needed)"
        }
        
        return cost_estimates.get(travel_mode, "$10-30")
    
    # Mock data methods for when API is unavailable
    
    def _get_mock_events(self, location: str, event_type: str) -> Dict[str, Any]:
        """Get mock events data"""
        import datetime
        import random
        
        mock_events = [
            {
                'title': 'Tech Meetup Downtown',
                'venue': f'{location} Community Center',
                'location': f'{location} downtown',
                'date': (datetime.datetime.now() + datetime.timedelta(days=7)).strftime('%Y-%m-%d'),
                'time': '18:00',
                'type': event_type,
                'description': 'Weekly technology meetup for professionals and students',
                'rating': 4.2,
                'distance': 5
            },
            {
                'title': 'Innovation Workshop',
                'venue': f'{location} University',
                'location': f'{location} university district',
                'date': (datetime.datetime.now() + datetime.timedelta(days=14)).strftime('%Y-%m-%d'),
                'time': '14:00',
                'type': event_type,
                'description': 'Hands-on workshop on emerging technologies',
                'rating': 4.5,
                'distance': 12
            }
        ]
        
        return {
            'success': True,
            'events': mock_events,
            'note': 'Mock data - connect Google Maps API for real events'
        }
    
    def _get_mock_universities(self, location: str) -> Dict[str, Any]:
        """Get mock universities data"""
        mock_universities = [
            {
                'name': f'{location} State University',
                'location': f'{location} university district',
                'rating': 4.1,
                'user_ratings_total': 1200,
                'types': ['university', 'establishment']
            },
            {
                'name': f'{location} Community College',
                'location': f'{location} downtown',
                'rating': 3.8,
                'user_ratings_total': 450,
                'types': ['school', 'establishment']
            }
        ]
        
        return {
            'success': True,
            'universities': mock_universities,
            'note': 'Mock data - connect Google Maps API for real university data'
        }
    
    def _get_mock_study_spots(self, location: str, spot_type: str) -> Dict[str, Any]:
        """Get mock study spots data"""
        mock_spots = [
            {
                'name': f'{location} Public Library',
                'location': f'{location} downtown',
                'type': 'library',
                'rating': 4.3,
                'user_ratings_total': 890,
                'price_level': 0
            },
            {
                'name': 'Student Cafe',
                'location': f'{location} university area',
                'type': 'cafe',
                'rating': 4.0,
                'user_ratings_total': 234,
                'price_level': 2
            },
            {
                'name': 'Quiet Study Space',
                'location': f'{location} business district',
                'type': 'library',
                'rating': 4.2,
                'user_ratings_total': 156,
                'price_level': 0
            }
        ]
        
        return {
            'success': True,
            'spots': mock_spots,
            'note': 'Mock data - connect Google Maps API for real study spot data'
        }
    
    def _get_mock_networking_events(self, location: str, field: str) -> Dict[str, Any]:
        """Get mock networking events data"""
        import datetime
        
        mock_events = [
            {
                'title': f'{field.title()} Professionals Meetup',
                'venue': f'{location} Business Center',
                'location': f'{location} business district',
                'date': (datetime.datetime.now() + datetime.timedelta(days=10)).strftime('%Y-%m-%d'),
                'time': '18:30',
                'field': field,
                'type': 'networking',
                'description': f'Monthly networking event for {field} professionals',
                'attendees_expected': 45,
                'cost': 'Free'
            },
            {
                'title': 'Young Professionals Network',
                'venue': f'{location} Conference Center',
                'location': f'{location} downtown',
                'date': (datetime.datetime.now() + datetime.timedelta(days=21)).strftime('%Y-%m-%d'),
                'time': '19:00',
                'field': field,
                'type': 'networking',
                'description': 'Networking event for young professionals and students',
                'attendees_expected': 80,
                'cost': '$15'
            }
        ]
        
        return {
            'success': True,
            'events': mock_events,
            'note': 'Mock data - connect Google Maps API for real networking events'
        }
    
    def _get_mock_route(self, start: str, destinations: List[str], travel_mode: str) -> Dict[str, Any]:
        """Get mock route data"""
        import random
        
        total_distance = len(destinations) * random.randint(5, 20)
        total_time = total_distance * 3  # 3 minutes per km
        
        return {
            'success': True,
            'route': {
                'destinations': destinations,
                'optimized_order': destinations,  # Simple order for mock
                'total_distance': total_distance,
                'total_duration': total_time,
                'travel_mode': travel_mode,
                'estimated_cost': self._estimate_travel_cost(total_distance, travel_mode)
            },
            'note': 'Mock data - connect Google Maps API for real route optimization'
        }

# Global instance
maps_service = MapsService()