"""
Hermione Chat API - Academic Q&A Assistant
Provides detailed academic explanations in Hermione's studious style
"""

from flask import Blueprint, request, jsonify
from services.gemini_chat import gemini_chat
from utils.verify_firebase import optional_auth
from utils.helpers import clean_text, safe_json_response, extract_keywords

hermione_bp = Blueprint('hermione', __name__)

@hermione_bp.route('/chat', methods=['POST'])
@optional_auth
def academic_chat():
    """Answer academic questions in Hermione's knowledgeable style"""
    try:
        data = request.get_json()
        
        if not data or 'question' not in data:
            return jsonify({'error': 'Question is required for academic assistance'}), 400
        
        question = clean_text(data['question'])
        
        if not question:
            return jsonify({'error': 'Valid question content is required'}), 400
        
        # Extract subject and difficulty level
        subject = data.get('subject', 'general')
        difficulty = data.get('difficulty', 'intermediate')
        
        # Generate academic context
        context = create_academic_context(question, subject, difficulty)
        
        # Get Hermione's response
        llm_response = gemini_chat.chat(
            prompt=question,
            context=context,
            personality='hermione'
        )
        
        if not llm_response['success']:
            return jsonify({
                'error': 'Hermione is temporarily busy in the library',
                'fallback_answer': get_fallback_academic_response(subject)
            }), 500
        
        # Extract keywords from the question for related topics
        keywords = extract_keywords(question)
        
        response_data = {
            'success': True,
            'answer': llm_response['response'],
            'subject': subject,
            'difficulty': difficulty,
            'keywords': keywords,
            'confidence': 'high',  # Hermione is always confident!
            'source_suggestions': get_source_suggestions(subject),
            'model_used': llm_response.get('model', 'unknown')
        }
        
        return safe_json_response(response_data)
        
    except Exception as e:
        return jsonify({
            'error': 'An unexpected error occurred in the academic chat',
            'details': str(e)
        }), 500

def create_academic_context(question: str, subject: str, difficulty: str) -> str:
    """Create academic context for LLM response"""
    return f"""You are Hermione Granger, brilliant and studious. 
    Answer this {subject} question at {difficulty} level with an enthusiastic tone:
    1. Clear, detailed, specific explanations
    2. Examples if helpful
    3. a brief list of related topics at end(just topic names)
    
    Be thorough but not overwhelming, and always encourage further learning."""


def get_source_suggestions(subject: str) -> list:
    """Get recommended sources for further study"""
    sources_by_subject = {
        'mathematics': [
            "Khan Academy - Comprehensive video lessons",
            "MIT OpenCourseWare - University-level content",
            "Paul's Online Math Notes - Clear explanations"
        ],
        'physics': [
            "Feynman Lectures - Conceptual understanding", 
            "PhET Simulations - Interactive experiments",
            "MIT Physics Courses - Rigorous treatment"
        ],
        'chemistry': [
            "Organic Chemistry Portal - Reaction mechanisms",
            "ChemCollective - Virtual labs",
            "NIST Chemistry WebBook - Reference data"
        ]
    }
    
    return sources_by_subject.get(subject, [
        "Wikipedia - General overview and references",
        "Google Scholar - Academic papers and research",
        "Educational YouTube channels - Visual explanations"
    ])



def get_fallback_academic_response(subject: str) -> str:
    """Provide fallback academic response"""
    return f"I'd love to help you explore {subject}! While I can't access my full library right now, I encourage you to break down complex problems into smaller parts, use visual aids when possible, and don't hesitate to ask for clarification on specific concepts."