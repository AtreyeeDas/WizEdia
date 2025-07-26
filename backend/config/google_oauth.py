"""
Google OAuth2 Configuration for Calendar API
Handles Google Calendar authentication and setup
"""

import os
import json
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

def get_google_oauth_flow():
    """Create Google OAuth2 flow for Calendar API"""
    try:
        client_config = {
            "web": {
                "client_id": os.getenv('GOOGLE_CLIENT_ID'),
                "client_secret": os.getenv('GOOGLE_CLIENT_SECRET'),
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
                "redirect_uris": ["http://localhost:5000/oauth/callback"]
            }
        }
        
        flow = Flow.from_client_config(
            client_config,
            scopes=SCOPES
        )
        flow.redirect_uri = "http://localhost:5000/oauth/callback"
        
        return flow
    except Exception as e:
        print(f"Error creating Google OAuth flow: {e}")
        return None

def build_calendar_service(credentials):
    """Build Google Calendar service with credentials"""
    try:
        service = build('calendar', 'v3', credentials=credentials)
        return service
    except Exception as e:
        print(f"Error building Calendar service: {e}")
        return None