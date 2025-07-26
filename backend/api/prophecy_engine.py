"""
Prophecy Engine API - Calendar and Event Management
Integrates with Google Calendar to provide exam alerts and event management
"""

from flask import Blueprint, request, jsonify
from services.calendar_utils import calendar_service
from utils.verify_firebase import require_auth, optional_auth
from utils.helpers import safe_json_response
import datetime

prophecy_bp = Blueprint('prophecy', __name__)

@prophecy_bp.route('/calendar-alerts', methods=['GET'])
@optional_auth
def get_calendar_alerts():
    """Get upcoming exam and assignment alerts from calendar"""
    try:
        # Get query parameters
        days_ahead = min(int(request.args.get('days_ahead', 7)), 30)  # Max 30 days
        user_id = request.args.get('user_id')
        
        # For authenticated users, we could get their specific calendar
        user_credentials = None
        if hasattr(request, 'user') and request.user:
            user_id = request.user.get('uid')
            # In a real implementation, retrieve stored OAuth credentials
            # user_credentials = get_user_calendar_credentials(user_id)
        
        # Get upcoming events
        events_result = calendar_service.get_upcoming_events(
            user_credentials=user_credentials,
            max_results=20
        )
        
        if not events_result['success']:
            return jsonify({
                'error': 'Failed to retrieve calendar events',
                'details': events_result.get('error', 'Unknown error'),
                'fallback_events': get_fallback_events()
            }), 500
        
        # Get exam-specific alerts
        exam_alerts = calendar_service.get_exam_alerts(days_ahead=days_ahead)
        
        # Categorize events
        categorized_events = categorize_calendar_events(events_result['events'])
        
        # Generate prophecy insights
        prophecy_insights = generate_prophecy_insights(categorized_events, days_ahead)
        
        response_data = {
            'success': True,
            'time_range': f'Next {days_ahead} days',
            'total_events': events_result['count'],
            'events': {
                'all_events': events_result['events'],
                'exam_alerts': exam_alerts.get('upcoming_exams', []),
                'categorized': categorized_events
            },
            'prophecy_insights': prophecy_insights,
            'study_recommendations': generate_study_recommendations(categorized_events),
            'urgent_actions': identify_urgent_actions(exam_alerts.get('upcoming_exams', [])),
            'calendar_connected': user_credentials is not None
        }
        
        # Add user-specific data
        if hasattr(request, 'user') and request.user:
            response_data['user_id'] = user_id
            response_data['personalized'] = True
        
        return safe_json_response(response_data)
        
    except Exception as e:
        return jsonify({
            'error': 'Prophecy Engine encountered an unexpected error',
            'details': str(e),
            'fallback_events': get_fallback_events()
        }), 500

@prophecy_bp.route('/study-schedule', methods=['POST'])
@optional_auth
def generate_study_schedule():
    """Generate optimized study schedule based on upcoming events"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'Schedule parameters are required'}), 400
        
        # Extract parameters
        study_hours_per_day = min(float(data.get('study_hours_per_day', 4)), 12)
        subjects = data.get('subjects', ['Mathematics', 'Physics', 'Chemistry'])
        start_date = data.get('start_date', datetime.date.today().isoformat())
        
        # Get calendar events for context
        events_result = calendar_service.get_upcoming_events(max_results=15)
        upcoming_exams = calendar_service.get_exam_alerts(days_ahead=14)
        
        # Generate schedule
        schedule = create_optimized_schedule(
            study_hours_per_day,
            subjects,
            start_date,
            events_result.get('events', []),
            upcoming_exams.get('upcoming_exams', [])
        )
        
        response_data = {
            'success': True,
            'schedule': schedule,
            'parameters': {
                'study_hours_per_day': study_hours_per_day,
                'subjects': subjects,
                'start_date': start_date
            },
            'optimization_tips': generate_optimization_tips(schedule),
            'productivity_insights': generate_productivity_insights(study_hours_per_day)
        }
        
        return safe_json_response(response_data)
        
    except Exception as e:
        return jsonify({
            'error': 'Study schedule generation failed',
            'details': str(e)
        }), 500

@prophecy_bp.route('/exam-countdown', methods=['GET'])
@optional_auth
def get_exam_countdown():
    """Get countdown to important exams with preparation status"""
    try:
        # Get upcoming exams
        exam_alerts = calendar_service.get_exam_alerts(days_ahead=30)
        upcoming_exams = exam_alerts.get('upcoming_exams', [])
        
        # Calculate countdown and preparation metrics
        exam_countdowns = []
        for exam in upcoming_exams:
            countdown_data = calculate_exam_countdown(exam)
            exam_countdowns.append(countdown_data)
        
        # Sort by urgency
        exam_countdowns.sort(key=lambda x: x['days_remaining'])
        
        # Generate preparation insights
        preparation_insights = generate_preparation_insights(exam_countdowns)
        
        response_data = {
            'success': True,
            'exam_countdowns': exam_countdowns[:10],  # Limit to 10 most urgent
            'total_exams': len(exam_countdowns),
            'preparation_insights': preparation_insights,
            'motivation_message': generate_motivation_message(exam_countdowns),
            'emergency_alerts': identify_emergency_alerts(exam_countdowns)
        }
        
        return safe_json_response(response_data)
        
    except Exception as e:
        return jsonify({
            'error': 'Exam countdown unavailable',
            'details': str(e)
        }), 500

@prophecy_bp.route('/deadlines', methods=['GET'])
@optional_auth
def get_deadline_tracker():
    """Track all types of deadlines (assignments, projects, applications)"""
    try:
        deadline_type = request.args.get('type', 'all')  # all, assignments, projects, applications
        days_ahead = min(int(request.args.get('days_ahead', 14)), 60)
        
        # Get events and filter by type
        events_result = calendar_service.get_upcoming_events(max_results=30)
        all_events = events_result.get('events', [])
        
        # Filter and categorize deadlines
        deadlines = extract_deadlines(all_events, deadline_type, days_ahead)
        
        # Sort by urgency and impact
        prioritized_deadlines = prioritize_deadlines(deadlines)
        
        # Generate action plan
        action_plan = generate_deadline_action_plan(prioritized_deadlines)
        
        response_data = {
            'success': True,
            'deadline_type': deadline_type,
            'time_range': f'Next {days_ahead} days',
            'deadlines': prioritized_deadlines,
            'action_plan': action_plan,
            'completion_strategy': generate_completion_strategy(prioritized_deadlines),
            'stress_management_tips': get_stress_management_tips(len(prioritized_deadlines))
        }
        
        return safe_json_response(response_data)
        
    except Exception as e:
        return jsonify({
            'error': 'Deadline tracking failed',
            'details': str(e)
        }), 500

@prophecy_bp.route('/calendar-integration', methods=['POST'])
@require_auth
def setup_calendar_integration():
    """Setup or update calendar integration for authenticated users"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'Integration settings are required'}), 400
        
        user_id = request.user.get('uid')
        calendar_provider = data.get('provider', 'google')
        notification_preferences = data.get('notifications', {})
        
        # In a real implementation, this would:
        # 1. Store user's OAuth tokens
        # 2. Set up webhook subscriptions
        # 3. Configure notification preferences
        
        # For now, return success with mock data
        integration_status = {
            'success': True,
            'user_id': user_id,
            'provider': calendar_provider,
            'status': 'connected',
            'last_sync': datetime.datetime.now().isoformat(),
            'notifications': notification_preferences,
            'features_enabled': [
                'Exam alerts',
                'Assignment reminders',
                'Study schedule optimization',
                'Deadline tracking'
            ]
        }
        
        return safe_json_response(integration_status)
        
    except Exception as e:
        return jsonify({
            'error': 'Calendar integration setup failed',
            'details': str(e)
        }), 500

def categorize_calendar_events(events: list) -> dict:
    """Categorize events by type"""
    categories = {
        'exams': [],
        'assignments': [],
        'classes': [],
        'study_sessions': [],
        'other': []
    }
    
    for event in events:
        title_lower = event.get('title', '').lower()
        description_lower = event.get('description', '').lower()
        
        if any(keyword in title_lower for keyword in ['exam', 'test', 'quiz', 'midterm', 'final']):
            categories['exams'].append(event)
        elif any(keyword in title_lower for keyword in ['assignment', 'homework', 'project', 'due']):
            categories['assignments'].append(event)
        elif any(keyword in title_lower for keyword in ['class', 'lecture', 'seminar', 'lab']):
            categories['classes'].append(event)
        elif any(keyword in title_lower for keyword in ['study', 'review', 'practice']):
            categories['study_sessions'].append(event)
        else:
            categories['other'].append(event)
    
    return categories

def generate_prophecy_insights(categorized_events: dict, days_ahead: int) -> list:
    """Generate prophetic insights about upcoming academic period"""
    insights = []
    
    exam_count = len(categorized_events['exams'])
    assignment_count = len(categorized_events['assignments'])
    
    # Workload analysis
    total_academic_events = exam_count + assignment_count
    if total_academic_events > 5:
        insights.append({
            'type': 'warning',
            'message': f"The next {days_ahead} days show {total_academic_events} academic commitments. Prioritization will be crucial.",
            'action': 'Create a detailed study schedule and eliminate non-essential activities'
        })
    elif total_academic_events == 0:
        insights.append({
            'type': 'opportunity',
            'message': "A lighter academic period ahead - perfect for getting ahead or deep learning.",
            'action': 'Use this time to strengthen weak areas or explore advanced topics'
        })
    
    # Exam clustering
    if exam_count > 2:
        insights.append({
            'type': 'strategic',
            'message': f"{exam_count} exams approaching. Consider interleaving study topics to improve retention.",
            'action': 'Plan study sessions that rotate between subjects every 45-60 minutes'
        })
    
    # Assignment management
    if assignment_count > 3:
        insights.append({
            'type': 'time_management',
            'message': f"{assignment_count} assignments due soon. Break large tasks into smaller chunks.",
            'action': 'Start with assignments that have the earliest due dates or highest impact'
        })
    
    return insights

def generate_study_recommendations(categorized_events: dict) -> list:
    """Generate study recommendations based on upcoming events"""
    recommendations = []
    
    # Exam-focused recommendations
    if categorized_events['exams']:
        recommendations.append({
            'priority': 'high',
            'type': 'exam_prep',
            'title': 'Active Recall Practice',
            'description': 'Use flashcards, practice tests, and teach-back methods for exam subjects',
            'time_required': '2-3 hours per exam subject'
        })
    
    # Assignment recommendations
    if categorized_events['assignments']:
        recommendations.append({
            'priority': 'medium',
            'type': 'assignment_planning',
            'title': 'Assignment Time Blocking',
            'description': 'Allocate specific time blocks for each assignment to avoid last-minute rushes',
            'time_required': '1-2 hours planning + execution time'
        })
    
    # General study recommendations
    recommendations.append({
        'priority': 'medium',
        'type': 'review_sessions',
        'title': 'Daily Review Sessions',
        'description': 'Spend 30 minutes each evening reviewing the day\'s learning',
        'time_required': '30 minutes daily'
    })
    
    return recommendations

def identify_urgent_actions(upcoming_exams: list) -> list:
    """Identify urgent actions based on exam timeline"""
    urgent_actions = []
    
    for exam in upcoming_exams:
        days_until = exam.get('days_until', 0)
        
        if days_until <= 2:
            urgent_actions.append({
                'type': 'immediate',
                'exam': exam['title'],
                'action': 'Focus on final review and practice problems',
                'priority': 'critical'
            })
        elif days_until <= 5:
            urgent_actions.append({
                'type': 'this_week',
                'exam': exam['title'],
                'action': 'Complete comprehensive study plan and practice tests',
                'priority': 'high'
            })
        elif days_until <= 10:
            urgent_actions.append({
                'type': 'preparation',
                'exam': exam['title'],
                'action': 'Begin intensive study sessions and gather study materials',
                'priority': 'medium'
            })
    
    return urgent_actions

def create_optimized_schedule(study_hours: float, subjects: list, start_date: str, events: list, exams: list) -> dict:
    """Create an optimized study schedule"""
    try:
        start = datetime.datetime.fromisoformat(start_date)
    except:
        start = datetime.datetime.now()
    
    # Calculate subject priorities based on upcoming exams
    subject_priorities = calculate_subject_priorities(subjects, exams)
    
    # Generate daily schedule for next 7 days
    daily_schedules = []
    for day_offset in range(7):
        current_date = start + datetime.timedelta(days=day_offset)
        
        # Check for conflicts with existing events
        daily_events = get_events_for_date(events, current_date.date())
        available_hours = study_hours - calculate_event_conflicts(daily_events)
        
        if available_hours > 0:
            daily_schedule = allocate_daily_study_time(
                available_hours,
                subject_priorities,
                current_date
            )
            daily_schedules.append(daily_schedule)
    
    return {
        'daily_schedules': daily_schedules,
        'subject_priorities': subject_priorities,
        'total_study_hours': study_hours * 7,
        'optimization_notes': generate_schedule_notes(daily_schedules)
    }

def calculate_subject_priorities(subjects: list, exams: list) -> dict:
    """Calculate priority scores for each subject"""
    priorities = {subject: 1.0 for subject in subjects}  # Base priority
    
    # Increase priority for subjects with upcoming exams
    for exam in exams:
        exam_title = exam.get('title', '').lower()
        days_until = exam.get('days_until', 30)
        
        for subject in subjects:
            if subject.lower() in exam_title:
                # Higher priority for closer exams
                urgency_multiplier = max(1.0, 10.0 / max(days_until, 1))
                priorities[subject] *= urgency_multiplier
    
    # Normalize priorities
    total_priority = sum(priorities.values())
    for subject in priorities:
        priorities[subject] = priorities[subject] / total_priority
    
    return priorities

def allocate_daily_study_time(available_hours: float, priorities: dict, date: datetime.datetime) -> dict:
    """Allocate study time for a specific day"""
    daily_allocation = {}
    
    for subject, priority in priorities.items():
        allocated_time = available_hours * priority
        if allocated_time >= 0.5:  # Minimum 30 minutes
            daily_allocation[subject] = {
                'hours': round(allocated_time, 1),
                'suggested_times': suggest_study_times(allocated_time),
                'study_method': suggest_study_method(subject, allocated_time)
            }
    
    return {
        'date': date.date().isoformat(),
        'total_hours': available_hours,
        'subjects': daily_allocation,
        'productivity_tips': get_daily_productivity_tips(date.weekday())
    }

def get_events_for_date(events: list, target_date: datetime.date) -> list:
    """Get events for a specific date"""
    daily_events = []
    
    for event in events:
        try:
            event_date_str = event.get('start_time', '')
            if event_date_str:
                event_date = datetime.datetime.fromisoformat(event_date_str.replace('Z', '+00:00')).date()
                if event_date == target_date:
                    daily_events.append(event)
        except:
            continue
    
    return daily_events

def calculate_event_conflicts(daily_events: list) -> float:
    """Calculate how many study hours are lost to scheduled events"""
    conflict_hours = 0
    
    for event in daily_events:
        # Assume each event reduces available study time
        if event.get('type') in ['exam', 'assignment']:
            conflict_hours += 2  # High-stress events reduce productivity
        elif event.get('type') == 'class':
            conflict_hours += 1  # Classes take time and energy
        else:
            conflict_hours += 0.5  # Other events have minimal impact
    
    return min(conflict_hours, 6)  # Max 6 hours of conflicts per day

def suggest_study_times(hours: float) -> list:
    """Suggest optimal study time blocks"""
    if hours >= 3:
        return ['9:00 AM - 11:00 AM', '2:00 PM - 4:00 PM', '7:00 PM - 8:00 PM']
    elif hours >= 2:
        return ['9:00 AM - 11:00 AM', '7:00 PM - 8:00 PM']
    else:
        return ['9:00 AM - 10:00 AM']

def suggest_study_method(subject: str, hours: float) -> str:
    """Suggest study method based on subject and time available"""
    subject_lower = subject.lower()
    
    if hours >= 2:
        if 'math' in subject_lower or 'physics' in subject_lower:
            return 'Problem-solving practice with theory review'
        elif 'history' in subject_lower or 'literature' in subject_lower:
            return 'Reading with note-taking and discussion'
        else:
            return 'Mixed: theory review + practical application'
    else:
        return 'Quick review and flashcard practice'

def get_daily_productivity_tips(weekday: int) -> list:
    """Get productivity tips based on day of week"""
    tips_by_day = {
        0: ['Monday motivation: Start with your most challenging subject'],  # Monday
        1: ['Tuesday focus: Use the momentum from Monday'],  # Tuesday
        2: ['Wednesday balance: Take breaks every 90 minutes'],  # Wednesday
        3: ['Thursday preparation: Review for end-of-week assessments'],  # Thursday
        4: ['Friday completion: Finish weekly goals and plan ahead'],  # Friday
        5: ['Saturday deep work: Tackle complex topics with fewer distractions'],  # Saturday
        6: ['Sunday review: Consolidate the week\'s learning']  # Sunday
    }
    
    return tips_by_day.get(weekday, ['Stay focused and take regular breaks'])

def generate_optimization_tips(schedule: dict) -> list:
    """Generate tips for optimizing the study schedule"""
    return [
        'Use the Pomodoro Technique: 25 minutes study + 5 minutes break',
        'Start with the most challenging subject when your energy is highest',
        'Review previous day\'s material for 10 minutes before starting new topics',
        'Use active recall: test yourself instead of just re-reading notes',
        'Take a 15-minute walk between different subjects to reset your brain'
    ]

def generate_productivity_insights(study_hours: float) -> dict:
    """Generate insights about study productivity"""
    if study_hours > 8:
        return {
            'assessment': 'High intensity schedule',
            'warning': 'Risk of burnout - ensure adequate breaks and sleep',
            'recommendation': 'Consider reducing hours or spreading over more days'
        }
    elif study_hours > 6:
        return {
            'assessment': 'Intensive but manageable',
            'tip': 'Use time-blocking and active learning techniques',
            'recommendation': 'Plan reward activities to maintain motivation'
        }
    elif study_hours > 3:
        return {
            'assessment': 'Balanced approach',
            'tip': 'Focus on high-impact study methods',
            'recommendation': 'Perfect for consistent daily progress'
        }
    else:
        return {
            'assessment': 'Light study load',
            'tip': 'Make every minute count with focused attention',
            'recommendation': 'Consider increasing time for faster progress'
        }

def calculate_exam_countdown(exam: dict) -> dict:
    """Calculate countdown data for an exam"""
    try:
        exam_date_str = exam.get('start_time', '')
        exam_date = datetime.datetime.fromisoformat(exam_date_str.replace('Z', '+00:00'))
        now = datetime.datetime.now(datetime.timezone.utc)
        
        time_remaining = exam_date - now
        days_remaining = time_remaining.days
        hours_remaining = time_remaining.seconds // 3600
        
        # Calculate preparation status (mock calculation)
        urgency_level = get_urgency_level(days_remaining)
        preparation_score = calculate_preparation_score(exam, days_remaining)
        
        return {
            'title': exam.get('title', 'Unknown Exam'),
            'date': exam_date.strftime('%Y-%m-%d'),
            'time': exam_date.strftime('%H:%M'),
            'days_remaining': days_remaining,
            'hours_remaining': hours_remaining,
            'urgency_level': urgency_level,
            'preparation_score': preparation_score,
            'study_recommendation': get_study_recommendation(days_remaining, preparation_score),
            'location': exam.get('location', 'TBA')
        }
        
    except Exception as e:
        return {
            'title': exam.get('title', 'Unknown Exam'),
            'error': f'Date parsing error: {str(e)}',
            'days_remaining': 0,
            'urgency_level': 'unknown'
        }

def get_urgency_level(days_remaining: int) -> str:
    """Determine urgency level based on days remaining"""
    if days_remaining <= 1:
        return 'critical'
    elif days_remaining <= 3:
        return 'high'
    elif days_remaining <= 7:
        return 'medium'
    else:
        return 'low'

def calculate_preparation_score(exam: dict, days_remaining: int) -> dict:
    """Calculate mock preparation score"""
    # In a real implementation, this would track actual study progress
    base_score = min(days_remaining * 10, 100)  # More time = higher base score
    
    # Random variation for demo
    import random
    actual_score = max(0, min(100, base_score + random.randint(-20, 20)))
    
    return {
        'score': actual_score,
        'level': 'excellent' if actual_score >= 80 else 'good' if actual_score >= 60 else 'needs_improvement',
        'areas_to_focus': get_focus_areas(exam.get('title', ''))
    }

def get_focus_areas(exam_title: str) -> list:
    """Get focus areas based on exam subject"""
    title_lower = exam_title.lower()
    
    if 'math' in title_lower:
        return ['Practice problems', 'Formula memorization', 'Proof techniques']
    elif 'physics' in title_lower:
        return ['Conceptual understanding', 'Problem-solving strategies', 'Unit conversions']
    elif 'chemistry' in title_lower:
        return ['Reaction mechanisms', 'Molecular structures', 'Stoichiometry']
    elif 'history' in title_lower:
        return ['Timeline memorization', 'Cause-effect relationships', 'Essay writing']
    else:
        return ['Key concepts review', 'Practice questions', 'Summary notes']

def get_study_recommendation(days_remaining: int, preparation_score: dict) -> str:
    """Get study recommendation based on time and preparation"""
    score = preparation_score['score']
    
    if days_remaining <= 1:
        if score >= 80:
            return 'Light review and confidence building exercises'
        else:
            return 'Focus on key concepts and formula sheets'
    elif days_remaining <= 3:
        if score >= 70:
            return 'Practice tests and weak area reinforcement'
        else:
            return 'Intensive review of core material'
    elif days_remaining <= 7:
        if score >= 60:
            return 'Comprehensive review with practice problems'
        else:
            return 'Study plan creation and topic prioritization'
    else:
        return 'Begin systematic preparation and material organization'

def generate_preparation_insights(exam_countdowns: list) -> dict:
    """Generate insights about overall exam preparation"""
    if not exam_countdowns:
        return {'message': 'No upcoming exams found'}
    
    critical_exams = [e for e in exam_countdowns if e.get('urgency_level') == 'critical']
    high_urgency = [e for e in exam_countdowns if e.get('urgency_level') == 'high']
    
    insights = {
        'total_exams': len(exam_countdowns),
        'critical_count': len(critical_exams),
        'high_urgency_count': len(high_urgency),
        'overall_preparedness': calculate_overall_preparedness(exam_countdowns),
        'time_management_status': assess_time_management(exam_countdowns)
    }
    
    return insights

def calculate_overall_preparedness(exam_countdowns: list) -> dict:
    """Calculate overall preparedness across all exams"""
    if not exam_countdowns:
        return {'level': 'unknown', 'score': 0}
    
    total_score = 0
    valid_scores = 0
    
    for exam in exam_countdowns:
        prep_score = exam.get('preparation_score', {})
        if 'score' in prep_score:
            total_score += prep_score['score']
            valid_scores += 1
    
    if valid_scores == 0:
        return {'level': 'unknown', 'score': 0}
    
    average_score = total_score / valid_scores
    
    return {
        'score': round(average_score, 1),
        'level': 'excellent' if average_score >= 80 else 'good' if average_score >= 60 else 'needs_improvement',
        'recommendation': get_overall_recommendation(average_score)
    }

def get_overall_recommendation(average_score: float) -> str:
    """Get overall study recommendation"""
    if average_score >= 80:
        return 'Maintain current study rhythm and focus on confidence building'
    elif average_score >= 60:
        return 'Increase study intensity and focus on weak areas'
    else:
        return 'Consider adjusting study methods and seeking additional help'

def assess_time_management(exam_countdowns: list) -> str:
    """Assess time management status"""
    critical_count = len([e for e in exam_countdowns if e.get('urgency_level') == 'critical'])
    high_count = len([e for e in exam_countdowns if e.get('urgency_level') == 'high'])
    
    if critical_count > 2:
        return 'Poor - multiple critical deadlines approaching'
    elif critical_count > 0 or high_count > 3:
        return 'Needs improvement - tight schedule ahead'
    elif high_count > 0:
        return 'Manageable - some pressure but controllable'
    else:
        return 'Excellent - well-planned schedule'

def generate_motivation_message(exam_countdowns: list) -> str:
    """Generate motivational message based on exam situation"""
    if not exam_countdowns:
        return "Great job staying ahead! Use this time to reinforce your learning and explore new topics."
    
    critical_count = len([e for e in exam_countdowns if e.get('urgency_level') == 'critical'])
    
    if critical_count > 0:
        return "You're in the final stretch! Focus your energy and trust your preparation. You've got this! 🏆"
    elif len(exam_countdowns) > 3:
        return "A busy period ahead, but you're well-positioned to succeed. Take it one exam at a time! 📚"
    else:
        return "You have a good balance of preparation time. Stay consistent and confident! ⭐"

def identify_emergency_alerts(exam_countdowns: list) -> list:
    """Identify situations requiring immediate attention"""
    alerts = []
    
    for exam in exam_countdowns:
        days_remaining = exam.get('days_remaining', 30)
        prep_score = exam.get('preparation_score', {}).get('score', 100)
        
        if days_remaining <= 1 and prep_score < 50:
            alerts.append({
                'type': 'critical_preparation',
                'exam': exam['title'],
                'message': 'Exam tomorrow with low preparation score',
                'action': 'Focus on key concepts and seek immediate help if needed'
            })
        elif days_remaining <= 2 and prep_score < 30:
            alerts.append({
                'type': 'urgent_preparation',
                'exam': exam['title'],
                'message': 'Very low preparation with little time remaining',
                'action': 'Consider study group or tutor assistance'
            })
    
    return alerts

def extract_deadlines(events: list, deadline_type: str, days_ahead: int) -> list:
    """Extract and filter deadlines from events"""
    deadlines = []
    cutoff_date = datetime.datetime.now() + datetime.timedelta(days=days_ahead)
    
    for event in events:
        try:
            event_date_str = event.get('start_time', '')
            event_date = datetime.datetime.fromisoformat(event_date_str.replace('Z', '+00:00'))
            
            if event_date <= cutoff_date:
                title_lower = event.get('title', '').lower()
                
                # Determine event type
                event_type = 'other'
                if any(keyword in title_lower for keyword in ['assignment', 'homework', 'due']):
                    event_type = 'assignment'
                elif any(keyword in title_lower for keyword in ['project', 'presentation']):
                    event_type = 'project'
                elif any(keyword in title_lower for keyword in ['application', 'deadline', 'submission']):
                    event_type = 'application'
                
                # Filter by requested type
                if deadline_type == 'all' or deadline_type == event_type:
                    deadline_data = {
                        'title': event.get('title', 'Unknown Deadline'),
                        'type': event_type,
                        'date': event_date.strftime('%Y-%m-%d'),
                        'time': event_date.strftime('%H:%M'),
                        'days_remaining': (event_date - datetime.datetime.now(datetime.timezone.utc)).days,
                        'description': event.get('description', ''),
                        'location': event.get('location', ''),
                        'urgency': get_urgency_level((event_date - datetime.datetime.now(datetime.timezone.utc)).days)
                    }
                    deadlines.append(deadline_data)
                    
        except Exception:
            continue
    
    return deadlines

def prioritize_deadlines(deadlines: list) -> list:
    """Sort deadlines by priority (urgency + impact)"""
    def priority_score(deadline):
        days_remaining = deadline.get('days_remaining', 30)
        urgency = deadline.get('urgency', 'low')
        
        # Urgency scoring
        urgency_scores = {'critical': 100, 'high': 75, 'medium': 50, 'low': 25}
        urgency_score = urgency_scores.get(urgency, 25)
        
        # Time pressure scoring (inverse of days remaining)
        time_pressure = max(0, 50 - days_remaining * 2)
        
        return urgency_score + time_pressure
    
    return sorted(deadlines, key=priority_score, reverse=True)

def generate_deadline_action_plan(deadlines: list) -> list:
    """Generate action plan for managing deadlines"""
    if not deadlines:
        return ['No immediate deadlines - great time to get ahead on future work!']
    
    action_plan = []
    
    # Group deadlines by urgency
    critical = [d for d in deadlines if d.get('urgency') == 'critical']
    high = [d for d in deadlines if d.get('urgency') == 'high']
    
    if critical:
        action_plan.append(f"IMMEDIATE: Complete {len(critical)} critical deadline(s) first")
        for deadline in critical[:3]:  # Show top 3
            action_plan.append(f"  • {deadline['title']} (Due: {deadline['date']})")
    
    if high:
        action_plan.append(f"THIS WEEK: Address {len(high)} high-priority deadline(s)")
        for deadline in high[:3]:  # Show top 3
            action_plan.append(f"  • {deadline['title']} (Due: {deadline['date']})")
    
    # General advice
    action_plan.extend([
        "Break large tasks into smaller, manageable chunks",
        "Set up daily check-ins to track progress",
        "Eliminate non-essential activities until deadlines are met"
    ])
    
    return action_plan

def generate_completion_strategy(deadlines: list) -> dict:
    """Generate strategy for completing all deadlines"""
    if not deadlines:
        return {'strategy': 'maintenance', 'description': 'Focus on staying ahead of future deadlines'}
    
    critical_count = len([d for d in deadlines if d.get('urgency') == 'critical'])
    high_count = len([d for d in deadlines if d.get('urgency') == 'high'])
    
    if critical_count > 2:
        return {
            'strategy': 'crisis_management',
            'description': 'Emergency mode: Focus only on critical deadlines, delegate or postpone everything else',
            'time_allocation': 'Dedicate 80% of time to critical tasks'
        }
    elif critical_count > 0 or high_count > 3:
        return {
            'strategy': 'sprint_mode',
            'description': 'Intensive focus: Complete urgent tasks first, then systematic progress on others',
            'time_allocation': 'Dedicate 60% of time to urgent tasks, 40% to important tasks'
        }
    else:
        return {
            'strategy': 'balanced_progression',
            'description': 'Steady progress: Work through deadlines systematically by priority',
            'time_allocation': 'Distribute time evenly based on task complexity and deadline proximity'
        }

def get_stress_management_tips(deadline_count: int) -> list:
    """Get stress management tips based on workload"""
    if deadline_count > 5:
        return [
            'Practice deep breathing exercises (4-7-8 technique)',
            'Take 10-minute breaks every hour to prevent burnout',
            'Prioritize sleep - even 15 minutes extra can improve focus',
            'Consider reaching out for help or deadline extensions if possible'
        ]
    elif deadline_count > 2:
        return [
            'Use the Pomodoro Technique to maintain focus',
            'Take short walks between tasks to clear your mind',
            'Stay hydrated and eat regular, healthy meals',
            'Celebrate small wins to maintain motivation'
        ]
    else:
        return [
            'Maintain your regular sleep and exercise routine',
            'Use this manageable workload to build good habits',
            'Consider helping others who might be more overwhelmed'
        ]

def get_fallback_events() -> list:
    """Provide fallback events when calendar is unavailable"""
    return [
        {
            'title': 'Sample Midterm Exam',
            'type': 'exam',
            'start_time': (datetime.datetime.now() + datetime.timedelta(days=5)).isoformat(),
            'description': 'Sample exam event - connect your calendar for real data'
        },
        {
            'title': 'Sample Assignment Due',
            'type': 'assignment',
            'start_time': (datetime.datetime.now() + datetime.timedelta(days=3)).isoformat(),
            'description': 'Sample assignment - connect your calendar for real data'
        }
    ]

def generate_schedule_notes(daily_schedules: list) -> list:
    """Generate notes about the schedule optimization"""
    return [
        'Schedule optimized based on exam priorities and available time',
        'Adjust timing based on your personal peak productivity hours',
        'Take 15-minute breaks between different subjects',
        'Review and adjust the schedule daily based on your progress'
    ]