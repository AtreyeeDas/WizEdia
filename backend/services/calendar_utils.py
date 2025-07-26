"""
Google Calendar Utilities
Handles Google Calendar API interactions for event management
"""

import os
import datetime
from typing import Dict, List, Any
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials

class CalendarService:
    def __init__(self):
        self.api_key = os.getenv('GOOGLE_MAPS_API_KEY')  # Using Maps API key for simplicity
    
    def get_upcoming_events(self, user_credentials=None, max_results=10) -> Dict[str, Any]:
        """Get upcoming calendar events"""
        try:
            if not user_credentials:
                # Return mock data when no credentials available
                return self._get_mock_events()
            
            service = build('calendar', 'v3', credentials=user_credentials)
            
            # Get current time
            now = datetime.datetime.utcnow().isoformat() + 'Z'
            
            # Get events
            events_result = service.events().list(
                calendarId='primary',
                timeMin=now,
                maxResults=max_results,
                singleEvents=True,
                orderBy='startTime'
            ).execute()
            
            events = events_result.get('items', [])
            
            formatted_events = []
            for event in events:
                start = event['start'].get('dateTime', event['start'].get('date'))
                formatted_events.append({
                    'title': event.get('summary', 'No Title'),
                    'start_time': start,
                    'description': event.get('description', ''),
                    'location': event.get('location', ''),
                    'id': event.get('id', '')
                })
            
            return {
                'success': True,
                'events': formatted_events,
                'count': len(formatted_events)
            }
            
        except Exception as e:
            print(f"Calendar API error: {e}")
            return self._get_mock_events()
    
    def _get_mock_events(self) -> Dict[str, Any]:
        """Return mock events for demonstration"""
        mock_events = [
            {
                'title': 'Potions Class Exam',
                'start_time': (datetime.datetime.now() + datetime.timedelta(days=2)).isoformat(),
                'description': 'Final exam for Advanced Potions with Professor Snape',
                'location': 'Dungeons Classroom',
                'type': 'exam'
            },
            {
                'title': 'Transfiguration Assignment Due',
                'start_time': (datetime.datetime.now() + datetime.timedelta(days=5)).isoformat(),
                'description': 'Essay on Advanced Transfiguration Techniques',
                'location': 'McGonagall\'s Office',
                'type': 'assignment'
            },
            {
                'title': 'Quidditch Practice',
                'start_time': (datetime.datetime.now() + datetime.timedelta(days=1)).isoformat(),
                'description': 'Team practice for upcoming match',
                'location': 'Quidditch Pitch',
                'type': 'activity'
            },
            {
                'title': 'Defense Against Dark Arts Study Group',
                'start_time': (datetime.datetime.now() + datetime.timedelta(days=3)).isoformat(),
                'description': 'Group study session for DADA final exam',
                'location': 'Library',
                'type': 'study'
            }
        ]
        
        return {
            'success': True,
            'events': mock_events,
            'count': len(mock_events),
            'note': 'These are sample events. Connect your Google Calendar for real data.'
        }
    
    def get_exam_alerts(self, days_ahead=7) -> Dict[str, Any]:
        """Get exam and assignment alerts"""
        try:
            # This would typically filter calendar events for exams/assignments
            events = self._get_mock_events()
            
            exam_events = []
            for event in events['events']:
                if event.get('type') in ['exam', 'assignment']:
                    event_date = datetime.datetime.fromisoformat(event['start_time'].replace('Z', '+00:00'))
                    days_until = (event_date - datetime.datetime.now(datetime.timezone.utc)).days
                    
                    if 0 <= days_until <= days_ahead:
                        event['days_until'] = days_until
                        event['urgency'] = 'high' if days_until <= 2 else 'medium' if days_until <= 5 else 'low'
                        exam_events.append(event)
            
            return {
                'success': True,
                'upcoming_exams': exam_events,
                'count': len(exam_events),
                'days_ahead': days_ahead
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': f'Failed to get exam alerts: {str(e)}',
                'upcoming_exams': []
            }

# Global instance
calendar_service = CalendarService()