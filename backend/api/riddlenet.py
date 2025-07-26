"""
RiddleNet API - Evolving Diary Companion
LLM-powered diary that adapts to user's emotional state and tone
"""

from flask import Blueprint, request, jsonify
from services.gemini_chat import gemini_chat
from services.hf_nlp import hf_nlp
from utils.verify_firebase import optional_auth
from utils.helpers import clean_text, safe_json_response

riddlenet_bp = Blueprint('riddlenet', __name__)

@riddlenet_bp.route('/respond', methods=['POST'])
@optional_auth
def diary_response():
    """Generate empathetic diary response using LLM"""
    try:
        data = request.get_json()
        
        if not data or 'entry' not in data:
            return jsonify({'error': 'Diary entry is required'}), 400
        
        entry = clean_text(data['entry'])
        
        if not entry:
            return jsonify({'error': 'Valid diary entry content is required'}), 400
        
        # Analyze emotion first to tailor response
        emotion_analysis = hf_nlp.analyze_emotion(entry)
        primary_emotion = emotion_analysis.get('primary_emotion', 'neutral')
        
        # Get user's preferred house style if provided
        #house_preference = data.get('house', 'ravenclaw').lower()
        
        # Generate contextual prompt for diary response
        context = create_diary_context(entry, primary_emotion, house_preference)
        
        # Get LLM response with riddlenet personality
        llm_response = gemini_chat.chat(
            prompt=entry,
            context=context,
            personality='riddlenet'
        )
        
        if not llm_response['success']:
            return jsonify({
                'error': 'The Dark Lord is temporarily on a quest',
                'fallback_response': get_fallback_diary_response(primary_emotion)
            }), 500
        
        response_data = {
            'success': True,
            'response': llm_response['response'],
            'detected_emotion': primary_emotion,
            #'house_tone': house_preference,
            'empathy_level': calculate_empathy_level(primary_emotion),
            'follow_up_questions': generate_follow_up_questions(primary_emotion),
            'model_used': llm_response.get('model', 'unknown')
        }
        
        # Add personalization for authenticated users
        if hasattr(request, 'user') and request.user:
            response_data['user_id'] = request.user.get('uid')
            response_data['personalized'] = True
        
        return safe_json_response(response_data)
        
    except Exception as e:
        return jsonify({
            'error': 'RiddleNet encountered an unexpected error',
            'details': str(e),
            'fallback_response': "Thank you for sharing with me. Your thoughts are valuable, and I'm here to listen."
        }), 500



def create_diary_context(entry: str, emotion: str, house: str) -> str:
    """Create context for LLM diary response"""
    house_traits = {
        'gryffindor': 'brave, encouraging, and bold',
        'hufflepuff': 'kind, patient, and loyal', 
        'ravenclaw': 'wise, analytical, and thoughtful',
        'slytherin': 'ambitious, clever, and strategic'
    }
    
    #trait = house_traits.get(house, 'wise and empathetic')
    
    return f"""You are an evolving diary companion responding to a {emotion} entry. 
    Respond in a kind and thoughtful tone, adapting to the user's emotional state. 
    Be supportive but honest, offering gentle insights without being preachy.
    Keep responses warm and conversational, as if talking to a close friend."""

def calculate_empathy_level(emotion: str) -> str:
    """Calculate appropriate empathy level based on emotion"""
    high_empathy_emotions = ['sadness', 'fear', 'anxiety', 'anger']
    medium_empathy_emotions = ['surprise', 'disgust']
    
    if emotion in high_empathy_emotions:
        return 'high'
    elif emotion in medium_empathy_emotions:
        return 'medium'
    else:
        return 'supportive'

def generate_follow_up_questions(emotion: str) -> list:
    """Generate thoughtful follow-up questions"""
    question_sets = {
        'sadness': [
            "What's one small thing that might bring you comfort right now?",
            "Have you experienced this feeling before? What helped then?"
        ],
        'anxiety': [
            "What aspects of this situation feel within your control?",
            "What would you tell a friend facing the same challenge?"
        ],
        'joy': [
            "What made this moment especially meaningful to you?", 
            "How can you carry this positive energy forward?"
        ],
        'anger': [
            "What boundary or value feels like it's been crossed?",
            "What would a constructive response look like for you?"
        ]
    }
    
    return question_sets.get(emotion, [
        "What's one thing you learned about yourself today?",
        "What are you most curious about right now?"
    ])

def get_fallback_diary_response(emotion: str) -> str:
    """Provide fallback response when LLM is unavailable"""
    fallback_responses = {
        'sadness': "I hear the weight in your words. Sadness is a natural part of the human experience, and it's okay to sit with these feelings. You're not alone in this.",
        'anxiety': "The uncertainty you're feeling is real and valid. Sometimes our minds create storms that feel overwhelming, but remember - storms do pass.",
        'joy': "Your happiness is contagious! It's beautiful when we take time to notice and celebrate the good moments in our lives.",
        'anger': "That fire you're feeling shows you care deeply about something. Anger often points us toward what matters most to us.",
        'fear': "Fear can feel paralyzing, but it also shows you're about to do something brave. Courage isn't the absence of fear - it's moving forward despite it."
    }
    
    return fallback_responses.get(emotion, "Thank you for sharing this moment with me. Your thoughts and feelings matter, and I'm honored you chose to express them here.")