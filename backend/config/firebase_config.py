"""
Firebase Admin SDK Configuration
Handles Firebase authentication and Firestore setup
"""

import os
import json
import base64
import firebase_admin
from firebase_admin import credentials, firestore, auth
from typing import Optional

def initialize_firebase():
    """Initialize Firebase Admin SDK with service account credentials"""
    try:
        # Check if Firebase is already initialized
        if firebase_admin._apps:
            return firebase_admin.get_app()
        
        # Get Firebase credentials from environment
        firebase_creds_json = os.getenv('FIREBASE_CREDENTIALS_JSON')
        
        if not firebase_creds_json:
            print("Warning: Firebase credentials not found. Some features may not work.")
            return None
        
        # Decode base64 credentials if needed
        try:
            if firebase_creds_json.startswith('eyJ'):  # Base64 encoded JSON
                decoded_creds = base64.b64decode(firebase_creds_json)
                creds_dict = json.loads(decoded_creds)
            else:
                creds_dict = json.loads(firebase_creds_json)
        except Exception as e:
            print(f"Error parsing Firebase credentials: {e}")
            return None
        
        # Initialize Firebase with credentials
        cred = credentials.Certificate(creds_dict)
        app = firebase_admin.initialize_app(cred)
        
        print("✅ Firebase initialized successfully!")
        return app
        
    except Exception as e:
        print(f"❌ Error initializing Firebase: {e}")
        return None

def get_firestore_client():
    """Get Firestore client instance"""
    try:
        return firestore.client()
    except Exception as e:
        print(f"Error getting Firestore client: {e}")
        return None

def verify_firebase_token(id_token: str) -> Optional[dict]:
    """Verify Firebase ID token and return user info"""
    try:
        decoded_token = auth.verify_id_token(id_token)
        return decoded_token
    except Exception as e:
        print(f"Error verifying Firebase token: {e}")
        return None