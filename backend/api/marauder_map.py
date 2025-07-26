"""
Marauder's Map API - Event Discovery and Location Services
Finds nearby educational events, hackathons, and conferences using Google Maps and Places API
"""

from flask import Blueprint, request, jsonify
from services.maps_utils import maps_service
from utils.verify_firebase import optional_auth
from utils.helpers import clean_text, safe_json_response
import datetime

marauder_bp = Blueprint('marauder', __name__)

@marauder_bp.route('/events', methods=['GET'])
@optional_auth
def find_nearby_events():
    """Find educational events, hackathons, and conferences near a location"""
    try:
        # Get query parameters
        location = request.args.get('location', 'New York')
        radius = min(int(request.args.get('radius', 50)), 200)  # Max 200km radius
        event_type = request.args.get('type', 'all')  # all, hackathons, conferences, workshops
        
        # Clean location input
        location = clean_text(location)
        if not location:
            return jsonify({'error': 'Valid location is required'}), 400
        
        # Find events using maps service
        events_result = maps_service.find_educational_events(
            location=location,
            radius=radius,
            event_type=event_type
        )
        
        if not events_result['success']:
            return jsonify({
                'error': 'Failed to find nearby events',
                'details': events_result.get('error', 'Unknown error'),
                'fallback_events': get_fallback_events(location)
            }), 500
        
        # Enhance events with additional data
        enhanced_events = enhance_event_data(events_result['events'])
        
        # Filter and sort events
        filtered_events = filter_events_by_relevance(enhanced_events, event_type)
        sorted_events = sort_events_by_priority(filtered_events)
        
        # Generate travel recommendations
        travel_recommendations = generate_travel_recommendations(location, sorted_events[:5])
        
        response_data = {
            'success': True,
            'search_location': location,
            'search_radius': f'{radius} km',
            'event_type': event_type,
            'total_events': len(sorted_events),
            'events': sorted_events[:20],  # Limit to 20 events
            'travel_recommendations': travel_recommendations,
            'location_insights': generate_location_insights(location),
            'search_tips': get_search_optimization_tips()
        }
        
        # Add user context if authenticated
        if hasattr(request, 'user') and request.user:
            response_data['user_id'] = request.user.get('uid')
            response_data['personalized_suggestions'] = get_personalized_suggestions(request.user)
        
        return safe_json_response(response_data)
        
    except Exception as e:
        return jsonify({
            'error': 'Event discovery encountered an unexpected error',
            'details': str(e),
            'fallback_events': get_fallback_events('your area')
        }), 500

@marauder_bp.route('/universities', methods=['GET'])
@optional_auth
def find_nearby_universities():
    """Find universities and educational institutions near a location"""
    try:
        location = request.args.get('location', 'Boston')
        radius = min(int(request.args.get('radius', 25)), 100)  # Max 100km for universities
        
        location = clean_text(location)
        if not location:
            return jsonify({'error': 'Valid location is required'}), 400
        
        # Find universities using maps service
        universities_result = maps_service.find_universities(
            location=location,
            radius=radius
        )
        
        if not universities_result['success']:
            return jsonify({
                'error': 'Failed to find universities',
                'fallback_universities': get_fallback_universities(location)
            }), 500
        
        # Enhance university data
        enhanced_universities = enhance_university_data(universities_result['universities'])
        
        response_data = {
            'success': True,
            'search_location': location,
            'search_radius': f'{radius} km',
            'total_universities': len(enhanced_universities),
            'universities': enhanced_universities[:15],  # Limit to 15
            'educational_ecosystem': analyze_educational_ecosystem(enhanced_universities),
            'study_opportunities': identify_study_opportunities(enhanced_universities)
        }
        
        return safe_json_response(response_data)
        
    except Exception as e:
        return jsonify({
            'error': 'University discovery failed',
            'details': str(e)
        }), 500

@marauder_bp.route('/study-spots', methods=['GET'])
@optional_auth
def find_study_locations():
    """Find libraries, cafes, and study-friendly locations"""
    try:
        location = request.args.get('location', 'Downtown')
        spot_type = request.args.get('spot_type', 'all')  # all, libraries, cafes, coworking
        
        location = clean_text(location)
        if not location:
            return jsonify({'error': 'Valid location is required'}), 400
        
        # Find study spots using maps service
        spots_result = maps_service.find_study_spots(
            location=location,
            spot_type=spot_type
        )
        
        if not spots_result['success']:
            return jsonify({
                'error': 'Failed to find study spots',
                'fallback_spots': get_fallback_study_spots(location)
            }), 500
        
        # Enhance spots with study-friendly features
        enhanced_spots = enhance_study_spot_data(spots_result['spots'])
        
        # Rate spots for study suitability
        rated_spots = rate_study_suitability(enhanced_spots)
        
        response_data = {
            'success': True,
            'search_location': location,
            'spot_type': spot_type,
            'total_spots': len(rated_spots),
            'study_spots': rated_spots[:15],
            'study_tips': get_study_location_tips(),
            'best_times': suggest_best_study_times(rated_spots)
        }
        
        return safe_json_response(response_data)
        
    except Exception as e:
        return jsonify({
            'error': 'Study spot discovery failed',
            'details': str(e)
        }), 500

@marauder_bp.route('/networking', methods=['GET'])
@optional_auth
def find_networking_opportunities():
    """Find meetups, conferences, and networking events for students and professionals"""
    try:
        location = request.args.get('location', 'San Francisco')
        field = request.args.get('field', 'technology')  # technology, business, science, arts
        
        location = clean_text(location)
        field = clean_text(field)
        
        if not location:
            return jsonify({'error': 'Valid location is required'}), 400
        
        # Find networking events
        networking_result = maps_service.find_networking_events(
            location=location,
            field=field
        )
        
        if not networking_result['success']:
            return jsonify({
                'error': 'Failed to find networking opportunities',
                'fallback_events': get_fallback_networking_events(location, field)
            }), 500
        
        # Categorize and enhance networking opportunities
        categorized_events = categorize_networking_events(networking_result['events'])
        
        # Generate networking strategy
        networking_strategy = generate_networking_strategy(field, categorized_events)
        
        response_data = {
            'success': True,
            'search_location': location,
            'field': field,
            'networking_opportunities': categorized_events,
            'networking_strategy': networking_strategy,
            'preparation_tips': get_networking_preparation_tips(),
            'follow_up_guidance': get_follow_up_guidance()
        }
        
        return safe_json_response(response_data)
        
    except Exception as e:
        return jsonify({
            'error': 'Networking discovery failed',
            'details': str(e)
        }), 500

@marauder_bp.route('/route-optimizer', methods=['POST'])
@optional_auth
def optimize_route():
    """Optimize route for visiting multiple educational locations"""
    try:
        data = request.get_json()
        
        if not data or 'destinations' not in data:
            return jsonify({'error': 'List of destinations is required'}), 400
        
        start_location = data.get('start_location', 'Current Location')
        destinations = data['destinations']
        travel_mode = data.get('travel_mode', 'driving')  # driving, transit, walking
        
        if len(destinations) > 10:
            return jsonify({'error': 'Maximum 10 destinations allowed'}), 400
        
        # Clean destinations
        clean_destinations = [clean_text(dest) for dest in destinations]
        clean_destinations = [dest for dest in clean_destinations if dest]
        
        if not clean_destinations:
            return jsonify({'error': 'Valid destinations are required'}), 400
        
        # Optimize route using maps service
        route_result = maps_service.optimize_multi_destination_route(
            start_location=start_location,
            destinations=clean_destinations,
            travel_mode=travel_mode
        )
        
        if not route_result['success']:
            return jsonify({
                'error': 'Route optimization failed',
                'fallback_route': create_simple_route(start_location, clean_destinations)
            }), 500
        
        # Enhance route with educational context
        enhanced_route = enhance_route_with_context(route_result['route'])
        
        # Generate travel insights
        travel_insights = generate_travel_insights(enhanced_route, travel_mode)
        
        response_data = {
            'success': True,
            'start_location': start_location,
            'travel_mode': travel_mode,
            'optimized_route': enhanced_route,
            'travel_insights': travel_insights,
            'time_management_tips': get_route_time_management_tips(),
            'backup_plans': generate_backup_plans(enhanced_route)
        }
        
        return safe_json_response(response_data)
        
    except Exception as e:
        return jsonify({
            'error': 'Route optimization failed',
            'details': str(e)
        }), 500

def enhance_event_data(events: list) -> list:
    """Enhance event data with additional context and ratings"""
    enhanced_events = []
    
    for event in events:
        enhanced_event = {
            **event,
            'educational_value': rate_educational_value(event),
            'networking_potential': rate_networking_potential(event),
            'career_relevance': rate_career_relevance(event),
            'accessibility': assess_accessibility(event),
            'cost_estimate': estimate_event_cost(event),
            'preparation_required': assess_preparation_required(event)
        }
        enhanced_events.append(enhanced_event)
    
    return enhanced_events

def filter_events_by_relevance(events: list, event_type: str) -> list:
    """Filter events based on type and relevance"""
    if event_type == 'all':
        return events
    
    filtered_events = []
    
    for event in events:
        event_title = event.get('title', '').lower()
        event_description = event.get('description', '').lower()
        
        if event_type == 'hackathons':
            if any(keyword in event_title or keyword in event_description 
                   for keyword in ['hackathon', 'hack', 'coding competition', 'dev challenge']):
                filtered_events.append(event)
        elif event_type == 'conferences':
            if any(keyword in event_title or keyword in event_description 
                   for keyword in ['conference', 'summit', 'symposium', 'convention']):
                filtered_events.append(event)
        elif event_type == 'workshops':
            if any(keyword in event_title or keyword in event_description 
                   for keyword in ['workshop', 'training', 'bootcamp', 'seminar']):
                filtered_events.append(event)
    
    return filtered_events

def sort_events_by_priority(events: list) -> list:
    """Sort events by priority score"""
    def calculate_priority_score(event):
        score = 0
        
        # Educational value weight
        score += event.get('educational_value', 0) * 3
        
        # Networking potential weight
        score += event.get('networking_potential', 0) * 2
        
        # Career relevance weight
        score += event.get('career_relevance', 0) * 2
        
        # Accessibility bonus
        if event.get('accessibility', {}).get('student_friendly', False):
            score += 10
        
        # Cost penalty (lower cost = higher score)
        cost = event.get('cost_estimate', {}).get('level', 'medium')
        if cost == 'free':
            score += 15
        elif cost == 'low':
            score += 10
        elif cost == 'medium':
            score += 5
        
        return score
    
    return sorted(events, key=calculate_priority_score, reverse=True)

def generate_travel_recommendations(location: str, top_events: list) -> dict:
    """Generate travel recommendations for attending events"""
    if not top_events:
        return {'message': 'No events found to generate travel recommendations'}
    
    # Calculate travel logistics
    nearby_events = [e for e in top_events if e.get('distance', 100) < 50]
    distant_events = [e for e in top_events if e.get('distance', 0) >= 50]
    
    recommendations = {
        'local_events': {
            'count': len(nearby_events),
            'suggestion': 'Perfect for day trips or after-class attendance',
            'preparation_time': '1-2 days'
        },
        'travel_required': {
            'count': len(distant_events),
            'suggestion': 'Plan weekend trips or longer stays for maximum value',
            'preparation_time': '1-2 weeks'
        },
        'budget_planning': generate_budget_recommendations(top_events),
        'time_optimization': generate_time_optimization_tips(top_events)
    }
    
    return recommendations

def generate_location_insights(location: str) -> dict:
    """Generate insights about the educational ecosystem in a location"""
    # This would typically use real data analysis
    # For now, providing structured insights
    
    location_lower = location.lower()
    
    # Major tech/education hubs
    if any(city in location_lower for city in ['san francisco', 'silicon valley', 'palo alto']):
        return {
            'ecosystem': 'tech_hub',
            'strength': 'Technology and entrepreneurship',
            'opportunity_density': 'very_high',
            'key_industries': ['Technology', 'AI/ML', 'Startups', 'VC'],
            'student_advantages': ['Internship opportunities', 'Networking density', 'Innovation exposure']
        }
    elif any(city in location_lower for city in ['boston', 'cambridge']):
        return {
            'ecosystem': 'academic_hub',
            'strength': 'Research and higher education',
            'opportunity_density': 'very_high',
            'key_industries': ['Biotech', 'Healthcare', 'Research', 'Education'],
            'student_advantages': ['University partnerships', 'Research opportunities', 'Academic conferences']
        }
    elif any(city in location_lower for city in ['new york', 'nyc']):
        return {
            'ecosystem': 'business_hub',
            'strength': 'Finance, media, and diverse industries',
            'opportunity_density': 'high',
            'key_industries': ['Finance', 'Media', 'Fashion', 'Real Estate'],
            'student_advantages': ['Industry diversity', 'Cultural events', 'Professional networking']
        }
    else:
        return {
            'ecosystem': 'emerging',
            'strength': 'Growing opportunities',
            'opportunity_density': 'moderate',
            'key_industries': ['Varies by local economy'],
            'student_advantages': ['Lower competition', 'Community building', 'Local impact potential']
        }

def get_search_optimization_tips() -> list:
    """Get tips for optimizing event searches"""
    return [
        'Use specific keywords related to your field of interest',
        'Search within 2-3 months ahead for best event availability',
        'Check university calendars for additional academic events',
        'Join professional associations for exclusive event access',
        'Follow event organizers on social media for early announcements'
    ]

def enhance_university_data(universities: list) -> list:
    """Enhance university data with educational context"""
    enhanced_universities = []
    
    for university in universities:
        enhanced_university = {
            **university,
            'academic_reputation': assess_academic_reputation(university),
            'research_opportunities': identify_research_opportunities(university),
            'student_resources': catalog_student_resources(university),
            'collaboration_potential': assess_collaboration_potential(university),
            'public_events': identify_public_events(university)
        }
        enhanced_universities.append(enhanced_university)
    
    return enhanced_universities

def analyze_educational_ecosystem(universities: list) -> dict:
    """Analyze the educational ecosystem in the area"""
    if not universities:
        return {'message': 'No universities found in the area'}
    
    # Categorize universities
    research_universities = [u for u in universities if u.get('academic_reputation', {}).get('research_focus', False)]
    liberal_arts = [u for u in universities if u.get('academic_reputation', {}).get('liberal_arts', False)]
    technical_schools = [u for u in universities if u.get('academic_reputation', {}).get('technical_focus', False)]
    
    return {
        'total_institutions': len(universities),
        'research_universities': len(research_universities),
        'liberal_arts_colleges': len(liberal_arts),
        'technical_schools': len(technical_schools),
        'ecosystem_strength': calculate_ecosystem_strength(universities),
        'collaboration_opportunities': identify_cross_university_opportunities(universities)
    }

def identify_study_opportunities(universities: list) -> list:
    """Identify study opportunities at universities"""
    opportunities = []
    
    for university in universities[:5]:  # Top 5 universities
        uni_opportunities = {
            'university': university.get('name', 'Unknown'),
            'opportunities': []
        }
        
        # Add different types of opportunities
        if university.get('public_events', {}).get('lectures', False):
            uni_opportunities['opportunities'].append('Public lectures and seminars')
        
        if university.get('student_resources', {}).get('library_access', False):
            uni_opportunities['opportunities'].append('Library and research facilities')
        
        if university.get('research_opportunities', {}).get('open_labs', False):
            uni_opportunities['opportunities'].append('Open research lab visits')
        
        if university.get('collaboration_potential', {}).get('student_exchange', False):
            uni_opportunities['opportunities'].append('Student exchange programs')
        
        if uni_opportunities['opportunities']:
            opportunities.append(uni_opportunities)
    
    return opportunities

def enhance_study_spot_data(spots: list) -> list:
    """Enhance study spot data with study-specific features"""
    enhanced_spots = []
    
    for spot in spots:
        enhanced_spot = {
            **spot,
            'wifi_quality': assess_wifi_quality(spot),
            'noise_level': assess_noise_level(spot),
            'seating_comfort': assess_seating_comfort(spot),
            'power_outlets': assess_power_availability(spot),
            'study_amenities': identify_study_amenities(spot),
            'peak_hours': identify_peak_hours(spot),
            'study_culture': assess_study_culture(spot)
        }
        enhanced_spots.append(enhanced_spot)
    
    return enhanced_spots

def rate_study_suitability(spots: list) -> list:
    """Rate spots for study suitability"""
    def calculate_study_score(spot):
        score = 0
        
        # Wifi quality (essential for modern studying)
        wifi = spot.get('wifi_quality', 'unknown')
        if wifi == 'excellent':
            score += 25
        elif wifi == 'good':
            score += 20
        elif wifi == 'fair':
            score += 10
        
        # Noise level (quiet is better for studying)
        noise = spot.get('noise_level', 'unknown')
        if noise == 'quiet':
            score += 25
        elif noise == 'moderate':
            score += 15
        elif noise == 'lively':
            score += 5
        
        # Seating comfort
        seating = spot.get('seating_comfort', 'unknown')
        if seating == 'excellent':
            score += 20
        elif seating == 'good':
            score += 15
        elif seating == 'fair':
            score += 10
        
        # Power outlets
        power = spot.get('power_outlets', 'unknown')
        if power == 'abundant':
            score += 15
        elif power == 'available':
            score += 10
        elif power == 'limited':
            score += 5
        
        # Study amenities bonus
        amenities = spot.get('study_amenities', {})
        if amenities.get('whiteboards', False):
            score += 5
        if amenities.get('group_rooms', False):
            score += 5
        if amenities.get('printing', False):
            score += 5
        
        return score
    
    for spot in spots:
        spot['study_suitability_score'] = calculate_study_score(spot)
        spot['study_rating'] = get_study_rating(spot['study_suitability_score'])
    
    return sorted(spots, key=lambda x: x['study_suitability_score'], reverse=True)

def get_study_location_tips() -> list:
    """Get tips for choosing and using study locations"""
    return [
        'Visit potential spots during your intended study hours to assess crowds',
        'Have backup locations in case your first choice is too busy',
        'Bring noise-canceling headphones for flexibility in any environment',
        'Check if locations offer student discounts or loyalty programs',
        'Respect the space and other patrons by keeping noise levels appropriate'
    ]

def suggest_best_study_times(spots: list) -> dict:
    """Suggest best study times based on spot characteristics"""
    suggestions = {}
    
    for spot in spots[:3]:  # Top 3 spots
        spot_name = spot.get('name', 'Unknown Location')
        spot_type = spot.get('type', 'unknown')
        
        if spot_type == 'library':
            suggestions[spot_name] = {
                'best_times': ['9:00 AM - 11:00 AM', '2:00 PM - 4:00 PM'],
                'avoid_times': ['12:00 PM - 1:00 PM (lunch rush)', '6:00 PM - 8:00 PM (evening peak)'],
                'tips': 'Libraries are usually quietest in the morning'
            }
        elif spot_type == 'cafe':
            suggestions[spot_name] = {
                'best_times': ['10:00 AM - 12:00 PM', '2:00 PM - 4:00 PM'],
                'avoid_times': ['7:00 AM - 9:00 AM (morning rush)', '5:00 PM - 7:00 PM (dinner rush)'],
                'tips': 'Mid-morning and afternoon are ideal for cafe studying'
            }
        else:
            suggestions[spot_name] = {
                'best_times': ['10:00 AM - 12:00 PM', '2:00 PM - 5:00 PM'],
                'avoid_times': ['12:00 PM - 1:00 PM', '6:00 PM - 8:00 PM'],
                'tips': 'Check specific location hours and peak times'
            }
    
    return suggestions

def categorize_networking_events(events: list) -> dict:
    """Categorize networking events by type and audience"""
    categories = {
        'professional_conferences': [],
        'student_meetups': [],
        'industry_workshops': [],
        'career_fairs': [],
        'social_events': []
    }
    
    for event in events:
        title_lower = event.get('title', '').lower()
        description_lower = event.get('description', '').lower()
        
        if any(keyword in title_lower for keyword in ['conference', 'summit', 'symposium']):
            categories['professional_conferences'].append(event)
        elif any(keyword in title_lower for keyword in ['student', 'college', 'university']):
            categories['student_meetups'].append(event)
        elif any(keyword in title_lower for keyword in ['workshop', 'training', 'bootcamp']):
            categories['industry_workshops'].append(event)
        elif any(keyword in title_lower for keyword in ['career fair', 'job fair', 'recruitment']):
            categories['career_fairs'].append(event)
        else:
            categories['social_events'].append(event)
    
    return categories

def generate_networking_strategy(field: str, categorized_events: dict) -> dict:
    """Generate networking strategy based on field and available events"""
    strategy = {
        'field': field,
        'primary_goals': get_field_networking_goals(field),
        'event_priorities': prioritize_event_types_for_field(field, categorized_events),
        'preparation_strategy': get_field_preparation_strategy(field),
        'follow_up_plan': get_field_follow_up_plan(field)
    }
    
    return strategy

def get_networking_preparation_tips() -> list:
    """Get general networking preparation tips"""
    return [
        'Research attendees and speakers beforehand using LinkedIn',
        'Prepare a 30-second elevator pitch about yourself',
        'Bring plenty of business cards or have a digital card ready',
        'Set specific goals: aim to have 3-5 meaningful conversations',
        'Prepare thoughtful questions about the industry or field',
        'Follow up within 48 hours with new connections'
    ]

def get_follow_up_guidance() -> dict:
    """Get guidance on following up after networking events"""
    return {
        'immediate_actions': [
            'Connect on LinkedIn within 24 hours',
            'Send personalized thank-you messages',
            'Organize contact information and notes'
        ],
        'within_week': [
            'Share relevant articles or resources mentioned',
            'Schedule follow-up coffee meetings',
            'Join any professional groups mentioned'
        ],
        'long_term': [
            'Add value to connections through introductions',
            'Share your own achievements and updates',
            'Maintain regular but not overwhelming contact'
        ]
    }

def enhance_route_with_context(route: dict) -> dict:
    """Enhance route with educational context"""
    enhanced_route = {
        **route,
        'educational_stops': identify_educational_stops_along_route(route),
        'study_breaks': suggest_study_break_locations(route),
        'time_optimization': optimize_time_for_learning(route),
        'backup_options': identify_backup_locations(route)
    }
    
    return enhanced_route

def generate_travel_insights(route: dict, travel_mode: str) -> dict:
    """Generate insights about the travel route"""
    total_time = route.get('total_duration', 0)
    total_distance = route.get('total_distance', 0)
    
    insights = {
        'efficiency_rating': calculate_route_efficiency(total_time, total_distance, travel_mode),
        'productivity_opportunities': identify_productivity_opportunities(route, travel_mode),
        'cost_analysis': analyze_travel_costs(route, travel_mode),
        'environmental_impact': assess_environmental_impact(travel_mode, total_distance)
    }
    
    return insights

def get_route_time_management_tips() -> list:
    """Get time management tips for multi-destination routes"""
    return [
        'Allow 15-30 minutes buffer time between locations',
        'Plan for parking or transportation delays',
        'Schedule most important destinations when you\'re most alert',
        'Use travel time for review or light study activities',
        'Have backup plans for each destination in case of closures'
    ]

def generate_backup_plans(route: dict) -> list:
    """Generate backup plans for route disruptions"""
    return [
        'Identify alternative transportation methods for each segment',
        'Research virtual alternatives for in-person events',
        'Plan for weather-related delays or cancellations',
        'Have contact information for all destinations',
        'Prepare offline materials in case of connectivity issues'
    ]

# Helper functions for rating and assessment

def rate_educational_value(event: dict) -> int:
    """Rate educational value of an event (0-100)"""
    title = event.get('title', '').lower()
    description = event.get('description', '').lower()
    
    score = 50  # Base score
    
    # Educational keywords boost
    educational_keywords = ['workshop', 'training', 'seminar', 'lecture', 'tutorial', 'masterclass']
    for keyword in educational_keywords:
        if keyword in title or keyword in description:
            score += 10
    
    # Technical/professional keywords
    tech_keywords = ['coding', 'programming', 'data', 'AI', 'machine learning', 'development']
    for keyword in tech_keywords:
        if keyword in title or keyword in description:
            score += 15
    
    return min(100, score)

def rate_networking_potential(event: dict) -> int:
    """Rate networking potential of an event (0-100)"""
    title = event.get('title', '').lower()
    description = event.get('description', '').lower()
    
    score = 40  # Base score
    
    # Networking indicators
    networking_keywords = ['networking', 'meetup', 'conference', 'mixer', 'social']
    for keyword in networking_keywords:
        if keyword in title or keyword in description:
            score += 15
    
    # Size indicators (larger events = more networking)
    size_keywords = ['conference', 'summit', 'convention', 'expo']
    for keyword in size_keywords:
        if keyword in title:
            score += 10
    
    return min(100, score)

def rate_career_relevance(event: dict) -> int:
    """Rate career relevance of an event (0-100)"""
    title = event.get('title', '').lower()
    description = event.get('description', '').lower()
    
    score = 45  # Base score
    
    # Career-focused keywords
    career_keywords = ['career', 'job', 'professional', 'industry', 'recruitment', 'hiring']
    for keyword in career_keywords:
        if keyword in title or keyword in description:
            score += 12
    
    # Skill development keywords
    skill_keywords = ['skills', 'certification', 'training', 'bootcamp', 'course']
    for keyword in skill_keywords:
        if keyword in title or keyword in description:
            score += 8
    
    return min(100, score)

def assess_accessibility(event: dict) -> dict:
    """Assess accessibility features of an event"""
    # Mock assessment - in real implementation, this would check actual accessibility data
    return {
        'student_friendly': True,  # Assume most educational events are student-friendly
        'wheelchair_accessible': True,  # Assume most venues are accessible
        'financial_aid_available': 'unknown',
        'transportation_accessible': True,
        'accommodation_friendly': 'unknown'
    }

def estimate_event_cost(event: dict) -> dict:
    """Estimate cost level of an event"""
    title = event.get('title', '').lower()
    description = event.get('description', '').lower()
    
    # Simple cost estimation based on keywords
    if any(keyword in title or keyword in description for keyword in ['free', 'no cost', 'complimentary']):
        return {'level': 'free', 'estimated_range': '$0'}
    elif any(keyword in title or keyword in description for keyword in ['student', 'university', 'college']):
        return {'level': 'low', 'estimated_range': '$0-50'}
    elif any(keyword in title or keyword in description for keyword in ['conference', 'summit', 'professional']):
        return {'level': 'medium', 'estimated_range': '$50-200'}
    else:
        return {'level': 'medium', 'estimated_range': '$25-100'}

def assess_preparation_required(event: dict) -> dict:
    """Assess preparation required for an event"""
    title = event.get('title', '').lower()
    description = event.get('description', '').lower()
    
    preparation_level = 'low'  # Default
    requirements = []
    
    if any(keyword in title or keyword in description for keyword in ['advanced', 'expert', 'professional']):
        preparation_level = 'high'
        requirements.extend(['Industry knowledge', 'Advanced skills'])
    elif any(keyword in title or keyword in description for keyword in ['intermediate', 'some experience']):
        preparation_level = 'medium'
        requirements.extend(['Basic knowledge', 'Some experience'])
    else:
        requirements.extend(['Open to beginners'])
    
    return {
        'level': preparation_level,
        'requirements': requirements,
        'suggested_prep_time': get_prep_time_suggestion(preparation_level)
    }

def get_prep_time_suggestion(level: str) -> str:
    """Get preparation time suggestion based on level"""
    if level == 'high':
        return '2-4 weeks'
    elif level == 'medium':
        return '1-2 weeks'
    else:
        return '1-3 days'

# Mock services and fallback data

def get_fallback_events(location: str) -> list:
    """Provide fallback events when service is unavailable"""
    return [
        {
            'title': f'Tech Meetup in {location}',
            'type': 'meetup',
            'date': (datetime.datetime.now() + datetime.timedelta(days=7)).strftime('%Y-%m-%d'),
            'location': f'{location} Community Center',
            'description': 'Monthly technology meetup for students and professionals',
            'educational_value': 75,
            'networking_potential': 85
        },
        {
            'title': f'Career Fair at {location} University',
            'type': 'career_fair',
            'date': (datetime.datetime.now() + datetime.timedelta(days=14)).strftime('%Y-%m-%d'),
            'location': f'{location} University Campus',
            'description': 'Annual career fair with 50+ employers',
            'educational_value': 60,
            'networking_potential': 90
        }
    ]

def get_fallback_universities(location: str) -> list:
    """Provide fallback university data"""
    return [
        {
            'name': f'{location} State University',
            'type': 'public_university',
            'location': f'{location} downtown',
            'academic_reputation': {'research_focus': True, 'ranking': 'regional'}
        },
        {
            'name': f'{location} Community College',
            'type': 'community_college',
            'location': f'{location} suburbs',
            'academic_reputation': {'vocational_focus': True, 'community_oriented': True}
        }
    ]

def get_fallback_study_spots(location: str) -> list:
    """Provide fallback study spot data"""
    return [
        {
            'name': f'{location} Public Library',
            'type': 'library',
            'location': f'{location} downtown',
            'wifi_quality': 'excellent',
            'noise_level': 'quiet'
        },
        {
            'name': f'Cafe Study in {location}',
            'type': 'cafe',
            'location': f'{location} university district',
            'wifi_quality': 'good',
            'noise_level': 'moderate'
        }
    ]

def get_fallback_networking_events(location: str, field: str) -> list:
    """Provide fallback networking events"""
    return [
        {
            'title': f'{field.title()} Professionals Meetup',
            'type': 'professional_meetup',
            'location': f'{location} business district',
            'date': (datetime.datetime.now() + datetime.timedelta(days=10)).strftime('%Y-%m-%d'),
            'description': f'Monthly networking event for {field} professionals and students'
        }
    ]

# Additional helper functions continue with similar mock implementations...

def create_simple_route(start: str, destinations: list) -> dict:
    """Create simple route as fallback"""
    return {
        'start_location': start,
        'destinations': destinations,
        'total_duration': len(destinations) * 30,  # Mock: 30 min per destination
        'total_distance': len(destinations) * 10,  # Mock: 10 km per destination
        'route_order': destinations,
        'note': 'Simplified route - connect to maps service for optimization'
    }

# Placeholder implementations for assessment functions
def assess_academic_reputation(university: dict) -> dict:
    return {'research_focus': True, 'ranking': 'regional', 'accreditation': 'accredited'}

def identify_research_opportunities(university: dict) -> dict:
    return {'open_labs': True, 'undergraduate_research': True, 'lab_tours': False}

def catalog_student_resources(university: dict) -> dict:
    return {'library_access': True, 'gym_facilities': False, 'study_spaces': True}

def assess_collaboration_potential(university: dict) -> dict:
    return {'student_exchange': True, 'joint_programs': False, 'research_partnerships': True}

def identify_public_events(university: dict) -> dict:
    return {'lectures': True, 'conferences': False, 'cultural_events': True}

def calculate_ecosystem_strength(universities: list) -> str:
    count = len(universities)
    if count >= 5:
        return 'strong'
    elif count >= 3:
        return 'moderate'
    else:
        return 'developing'

def identify_cross_university_opportunities(universities: list) -> list:
    return ['Inter-university conferences', 'Student exchange programs', 'Collaborative research projects']

def assess_wifi_quality(spot: dict) -> str:
    return 'good'  # Mock assessment

def assess_noise_level(spot: dict) -> str:
    spot_type = spot.get('type', '')
    if spot_type == 'library':
        return 'quiet'
    elif spot_type == 'cafe':
        return 'moderate'
    else:
        return 'unknown'

def assess_seating_comfort(spot: dict) -> str:
    return 'good'  # Mock assessment

def assess_power_availability(spot: dict) -> str:
    return 'available'  # Mock assessment

def identify_study_amenities(spot: dict) -> dict:
    return {'whiteboards': False, 'group_rooms': True, 'printing': False}

def identify_peak_hours(spot: dict) -> list:
    return ['12:00 PM - 2:00 PM', '6:00 PM - 8:00 PM']

def assess_study_culture(spot: dict) -> str:
    return 'study_friendly'

def get_study_rating(score: int) -> str:
    if score >= 80:
        return 'excellent'
    elif score >= 60:
        return 'good'
    elif score >= 40:
        return 'fair'
    else:
        return 'poor'

def get_field_networking_goals(field: str) -> list:
    goals = {
        'technology': ['Learn about emerging technologies', 'Connect with developers and engineers', 'Discover job opportunities'],
        'business': ['Build professional network', 'Learn about market trends', 'Find mentorship opportunities'],
        'science': ['Connect with researchers', 'Learn about funding opportunities', 'Discover collaboration possibilities']
    }
    return goals.get(field, ['Build professional connections', 'Learn about industry trends', 'Discover opportunities'])

def prioritize_event_types_for_field(field: str, events: dict) -> list:
    # Return prioritized list of event types for the field
    if field == 'technology':
        return ['industry_workshops', 'professional_conferences', 'student_meetups', 'career_fairs']
    else:
        return ['professional_conferences', 'industry_workshops', 'career_fairs', 'student_meetups']

def get_field_preparation_strategy(field: str) -> list:
    return [
        f'Research key companies and trends in {field}',
        'Prepare questions about career paths and skills needed',
        'Update portfolio or resume with relevant projects',
        'Practice discussing your interests and goals'
    ]

def get_field_follow_up_plan(field: str) -> list:
    return [
        'Connect on LinkedIn with personalized messages',
        'Send thank-you emails within 24 hours',
        'Schedule informational interviews with interesting contacts',
        'Join relevant professional associations mentioned'
    ]

def identify_educational_stops_along_route(route: dict) -> list:
    return ['University library', 'Science museum', 'Technology center']

def suggest_study_break_locations(route: dict) -> list:
    return ['Park with benches', 'Quiet cafe', 'Library reading room']

def optimize_time_for_learning(route: dict) -> dict:
    return {'suggested_schedule': 'Plan 2-3 hours per major destination', 'break_frequency': 'Every 90 minutes'}

def identify_backup_locations(route: dict) -> list:
    return ['Alternative libraries', 'Backup study cafes', 'University visitor centers']

def calculate_route_efficiency(time: int, distance: int, mode: str) -> str:
    return 'good'  # Mock efficiency rating

def identify_productivity_opportunities(route: dict, mode: str) -> list:
    if mode == 'transit':
        return ['Review notes during travel', 'Listen to educational podcasts', 'Use mobile learning apps']
    else:
        return ['Plan stops at educational locations', 'Use breaks for quick review sessions']

def analyze_travel_costs(route: dict, mode: str) -> dict:
    return {'estimated_cost': '$20-40', 'cost_factors': ['Fuel/transit fare', 'Parking fees', 'Food/beverages']}

def assess_environmental_impact(mode: str, distance: int) -> dict:
    impact = {
        'transit': 'low',
        'walking': 'minimal',
        'driving': 'moderate'
    }
    return {'level': impact.get(mode, 'unknown'), 'suggestions': ['Consider carpooling', 'Use public transit when possible']}

def generate_budget_recommendations(events: list) -> dict:
    return {
        'budget_range': '$0-200 per month',
        'priority_allocation': 'Focus on free events and student discounts',
        'cost_saving_tips': ['Look for student pricing', 'Attend free networking events', 'Share transportation costs']
    }

def generate_time_optimization_tips(events: list) -> list:
    return [
        'Group events by location to minimize travel',
        'Schedule high-energy events when you\'re most alert',
        'Leave buffer time between events for networking',
        'Plan study time around event schedules'
    ]