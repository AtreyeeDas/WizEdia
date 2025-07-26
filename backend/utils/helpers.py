"""
Common Utility Functions
Helper functions used across the application
"""

import re
import json
from typing import List, Dict, Any

def clean_text(text: str) -> str:
    """Clean and normalize text input"""
    if not text:
        return ""
    
    # Remove extra whitespace and normalize
    text = re.sub(r'\s+', ' ', text.strip())
    
    # Remove potentially harmful characters
    text = re.sub(r'[<>"\']', '', text)
    
    return text

def validate_email(email: str) -> bool:
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))

def safe_json_response(data: Any, status_code: int = 200) -> tuple:
    """Safely create JSON response with error handling"""
    try:
        if isinstance(data, str):
            data = {'message': data}
        return data, status_code
    except Exception as e:
        return {'error': f'Response formatting error: {str(e)}'}, 500

def extract_keywords(text: str, max_keywords: int = 5) -> List[str]:
    """Extract key terms from text"""
    if not text:
        return []
    
    # Simple keyword extraction (can be enhanced with NLP libraries)
    words = re.findall(r'\b[a-zA-Z]{3,}\b', text.lower())
    
    # Filter common stop words
    stop_words = {'the', 'and', 'but', 'for', 'with', 'this', 'that', 'will', 'you', 'are', 'was', 'were'}
    keywords = [word for word in words if word not in stop_words]
    
    # Return unique keywords up to max_keywords
    return list(dict.fromkeys(keywords))[:max_keywords]

def format_house_response(house: str) -> Dict[str, str]:
    """Format response in Hogwarts house style"""
    house_styles = {
        'gryffindor': {
            'tone': 'brave and encouraging',
            'emoji': '🦁',
            'color': '#740001'
        },
        'hufflepuff': {
            'tone': 'kind and patient',
            'emoji': '🦡',
            'color': '#ffdb00'
        },
        'ravenclaw': {
            'tone': 'wise and analytical',
            'emoji': '🦅',
            'color': '#0e1a40'
        },
        'slytherin': {
            'tone': 'ambitious and clever',
            'emoji': '🐍',
            'color': '#1a472a'
        }
    }
    
    return house_styles.get(house.lower(), house_styles['gryffindor'])