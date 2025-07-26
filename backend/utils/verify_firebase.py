"""
Firebase Authentication Utilities
Decorators and helpers for securing endpoints
"""

import functools
from flask import request, jsonify
from config.firebase_config import verify_firebase_token

def require_auth(f):
    """Decorator to require Firebase authentication"""
    @functools.wraps(f)
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        
        if not auth_header:
            return jsonify({'error': 'Authorization header missing'}), 401
        
        if not auth_header.startswith('Bearer '):
            return jsonify({'error': 'Invalid authorization format'}), 401
        
        id_token = auth_header.split('Bearer ')[1]
        
        user_info = verify_firebase_token(id_token)
        if not user_info:
            return jsonify({'error': 'Invalid or expired token'}), 401
        
        # Add user info to request context
        request.user = user_info
        return f(*args, **kwargs)
    
    return decorated_function

def optional_auth(f):
    """Decorator for optional authentication"""
    @functools.wraps(f)
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        
        if auth_header and auth_header.startswith('Bearer '):
            id_token = auth_header.split('Bearer ')[1]
            user_info = verify_firebase_token(id_token)
            request.user = user_info if user_info else None
        else:
            request.user = None
        
        return f(*args, **kwargs)
    
    return decorated_function