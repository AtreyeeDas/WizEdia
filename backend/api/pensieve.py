"""
Pensieve API - Emotion Analysis from Journal Entries
Analyzes emotional tone using Hugging Face emotion models
"""

from flask import Blueprint, request, jsonify
from services.hf_nlp import hf_nlp
from utils.verify_firebase import optional_auth
from utils.helpers import clean_text, safe_json_response

pensieve_bp = Blueprint('pensieve', __name__)

@pensieve_bp.route('/analyze', methods=['POST'])
@optional_auth
def analyze_emotion():
    """Analyze emotions in journal text using Hugging Face models"""
    try:
        data = request.get_json()
        
        if not data or 'text' not in data:
            return jsonify({'error': 'Text is required for emotion analysis'}), 400
        
        text = clean_text(data['text'])
        
        if not text:
            return jsonify({'error': 'Valid text content is required'}), 400
        
        # Analyze emotions using Hugging Face
        emotion_result = hf_nlp.analyze_emotion(text)
        
        if not emotion_result['success']:
            return jsonify({
                'error': 'Emotion analysis failed',
                'details': emotion_result.get('error', 'Unknown error'),
                'fallback_emotions': [
                    {'label': 'neutral', 'score': 0.5}
                ]
            }), 500
        
        # Add magical response based on emotions
        primary_emotion = emotion_result.get('primary_emotion', 'neutral')
        magical_response = get_magical_emotion_response(primary_emotion)
        
        response_data = {
            'success': True,
            'emotions': emotion_result['emotions'],
            'primary_emotion': primary_emotion,
            'confidence': emotion_result.get('confidence', 0.0),
            'magical_insight': magical_response,
            'house_suggestion': get_house_by_emotion(primary_emotion)
        }
        
        # Add user context if authenticated
        if hasattr(request, 'user') and request.user:
            response_data['user_id'] = request.user.get('uid')
        
        return safe_json_response(response_data)
        
    except Exception as e:
        return jsonify({
            'error': 'Pensieve analysis encountered an unexpected error',
            'details': str(e)
        }), 500

@pensieve_bp.route('/history', methods=['GET'])
@optional_auth

def get_magical_emotion_response(emotion: str) -> str:
    """Get magical response based on detected emotion"""
    responses = {
        'joy': "Your happiness radiates like a Patronus! ✨ Keep spreading this positive energy.",
        'sadness': "Even in the darkest times, remember that happiness can be found. 🕯️",
        'anger': "Channel that fire within you constructively, like a true Gryffindor. 🔥",
        'fear': "Courage is not the absence of fear, but facing it head-on. You've got this! 🦁",
        'surprise': "Life is full of magical surprises! Embrace the unexpected. 🌟",
        'disgust': "Sometimes we must face unpleasant truths to grow stronger. 🌱",
        'neutral': "A calm mind is like still water - it reflects clearly. 🌊"
    }
    
    return responses.get(emotion, "Every emotion teaches us something valuable. 📚")

def get_house_by_emotion(emotion: str) -> str:
    """Suggest Hogwarts house based on primary emotion"""
    house_mapping = {
        'joy': 'Hufflepuff',
        'anger': 'Gryffindor', 
        'fear': 'Ravenclaw',
        'sadness': 'Hufflepuff',
        'surprise': 'Ravenclaw',
        'disgust': 'Slytherin',
        'neutral': 'Ravenclaw'
    }
    
    return house_mapping.get(emotion, 'Ravenclaw')