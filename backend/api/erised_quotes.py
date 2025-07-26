"""
Mirror of Erised API - Motivational Quotes
Provides personalized motivational quotes based on user context and emotions
"""

import random
from flask import Blueprint, request, jsonify
from services.gemini_chat import gemini_chat
from utils.verify_firebase import optional_auth
from utils.helpers import safe_json_response
from markupsafe import escape
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address


erised_bp = Blueprint('erised', __name__)

# Create a limiter instance (without attaching to app yet)
limiter = Limiter(key_func=get_remote_address)

@erised_bp.route('/quote', methods=['GET'])
@limiter.limit("10 per minute")
@optional_auth
def get_motivational_quote():
    """Get a personalized motivational quote"""
    try:
        # Get optional parameters
        from markupsafe import escape

        mood = escape(request.args.get('mood', 'neutral'))
        context = escape(request.args.get('context', 'general'))
        house = escape(request.args.get('house', 'ravenclaw'))

        
        # Try to generate personalized quote using LLM
        if mood != 'neutral' or context != 'general':
            personalized_quote = generate_personalized_quote(mood, context, house)
            if personalized_quote:
                return safe_json_response(personalized_quote)
        
        # Fallback to curated quotes
        quote_data = get_curated_quote(mood, context, house)
        
        # Add user context if authenticated
        if hasattr(request, 'user') and request.user:
            quote_data['user_id'] = request.user.get('uid')
            quote_data['personalized'] = True
        
        return safe_json_response(quote_data)
        
    except Exception as e:
        return jsonify({
            'error': 'The Mirror of Erised is clouded at the moment',
            'details': str(e),
            'fallback_quote': {
                'text': "It does not do to dwell on dreams and forget to live.",
                'author': 'Albus Dumbledore',
                'source': 'Harry Potter and the Philosopher\'s Stone'
            }
        }), 500

@erised_bp.route('/daily', methods=['GET'])
@optional_auth
def get_daily_quote():
    """Get quote of the day"""
    try:
        # Generate daily quote based on date
        import datetime
        today = datetime.date.today()
        day_of_year = today.timetuple().tm_yday
        
        # Use day of year to select consistent daily quote
        daily_quotes = get_daily_quote_collection()
        selected_quote = daily_quotes[day_of_year % len(daily_quotes)]
        
        response_data = {
            'success': True,
            'type': 'daily_quote',
            'date': today.isoformat(),
            'quote': selected_quote['text'],
            'author': selected_quote['author'],
            'theme': selected_quote['theme'],
            'reflection_prompt': selected_quote.get('reflection', ''),
            'house_wisdom': get_house_wisdom(selected_quote['theme'])
        }
        
        return safe_json_response(response_data)
        
    except Exception as e:
        return jsonify({
            'error': 'Daily quote unavailable',
            'details': str(e)
        }), 500

@erised_bp.route('/themed', methods=['GET'])
def get_themed_quotes():
    """Get quotes organized by themes"""
    try:
        theme = request.args.get('theme', 'courage')
        limit = min(int(request.args.get('limit', 5)), 20)  # Max 20 quotes
        
        themed_quotes = get_quotes_by_theme(theme, limit)
        
        return jsonify({
            'success': True,
            'theme': theme,
            'quotes': themed_quotes,
            'count': len(themed_quotes),
            'available_themes': list(get_theme_categories().keys())
        })
        
    except Exception as e:
        return jsonify({
            'error': f'Failed to retrieve {theme} quotes',
            'details': str(e)
        }), 500

@erised_bp.route('/custom', methods=['POST'])
@optional_auth
def create_custom_quote():
    """Generate a custom motivational quote based on user's specific situation"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'Request data is required'}), 400
        
        situation = data.get('situation', '')
        goal = data.get('goal', '')
        challenge = data.get('challenge', '')
        preferred_style = data.get('style', 'inspiring')
        
        # Create personalized prompt
        prompt = create_custom_quote_prompt(situation, goal, challenge, preferred_style)
        
        # Generate quote using LLM
        llm_response = gemini_chat.chat(
            prompt=prompt,
            context="You are the Mirror of Erised, showing people what they need to hear to move forward.",
            personality='motivational'
        )
        
        if llm_response['success']:
            # Parse the generated quote
            quote_text = llm_response['response']
            
            response_data = {
                'success': True,
                'type': 'custom_generated',
                'quote': quote_text,
                'situation': situation,
                'goal': goal,
                'challenge': challenge,
                'style': preferred_style,
                'personalized': True,
                'mirror_insight': generate_mirror_insight(situation, goal)
            }
        else:
            # Fallback to template-based custom quote
            response_data = generate_template_quote(situation, goal, challenge, preferred_style)
            response_data['llm_fallback'] = True
        
        # Add user tracking
        if hasattr(request, 'user') and request.user:
            response_data['user_id'] = request.user.get('uid')
        
        return safe_json_response(response_data)
        
    except Exception as e:
        return jsonify({
            'error': 'Custom quote generation failed',
            'details': str(e)
        }), 500

@erised_bp.route('/reflection', methods=['POST'])
@optional_auth
def quote_reflection():
    """Provide guided reflection based on a quote"""
    try:
        data = request.get_json()
        
        if not data or 'quote' not in data:
            return jsonify({'error': 'Quote text is required for reflection'}), 400
        
        quote = data['quote']
        personal_context = data.get('context', '')
        
        # Generate reflection questions
        reflection_prompt = f"""Based on this quote: "{quote}"
        
        Personal context: {personal_context}
        
        Provide 3-4 thoughtful reflection questions that help the person apply this wisdom to their life."""
        
        reflection_response = gemini_chat.chat(
            prompt=reflection_prompt,
            context="You are a wise mentor helping someone reflect deeply on meaningful quotes.",
            personality='professor'
        )
        
        if reflection_response['success']:
            reflection_questions = reflection_response['response'].split('\n')
            reflection_questions = [q.strip() for q in reflection_questions if q.strip()]
        else:
            reflection_questions = generate_default_reflection_questions(quote)
        
        response_data = {
            'success': True,
            'quote': quote,
            'reflection_questions': reflection_questions,
            'journaling_prompts': generate_journaling_prompts(quote),
            'action_suggestions': generate_action_suggestions(quote),
            'related_wisdom': find_related_quotes(quote)
        }
        
        return safe_json_response(response_data)
        
    except Exception as e:
        return jsonify({
            'error': 'Reflection generation failed',
            'details': str(e)
        }), 500

def generate_personalized_quote(mood: str, context: str, house: str) -> dict:
    """Generate personalized quote using LLM"""
    try:
        house_style = get_house_style(house)
        
        prompt = f"""Generate an inspiring quote for someone who is feeling {mood} in the context of {context}. 
        Style it in the {house_style} manner of {house} house.
        
        Make it original, meaningful, and actionable. Include both the quote and a brief explanation of how to apply it."""
        
        llm_response = gemini_chat.chat(
            prompt=prompt,
            context="You are the Mirror of Erised, providing exactly what someone needs to hear.",
            personality='motivational'
        )
        
        if llm_response['success']:
            return {
                'success': True,
                'type': 'personalized',
                'quote': llm_response['response'],
                'mood': mood,
                'context': context,
                'house': house,
                'generated': True
            }
        
        return None
        
    except Exception:
        return None

def get_curated_quote(mood: str, context: str, house: str) -> dict:
    """Get curated quote from predefined collection"""
    quotes_by_mood = {
        'anxious': [
            {
                'text': "You are braver than you believe, stronger than you seem, and smarter than you think.",
                'author': 'A.A. Milne',
                'theme': 'courage',
                'application': 'Remember this when self-doubt creeps in'
            },
            {
                'text': "The cave you fear to enter holds the treasure you seek.",
                'author': 'Joseph Campbell',
                'theme': 'growth',
                'application': 'Face your fears - they guard your greatest opportunities'
            }
        ],
        'sad': [
            {
                'text': "Even the darkest night will end and the sun will rise.",
                'author': 'Victor Hugo',
                'theme': 'hope',
                'application': 'This feeling is temporary - better days are coming'
            },
            {
                'text': "The wound is the place where the Light enters you.",
                'author': 'Rumi',
                'theme': 'healing',
                'application': 'Your struggles are creating space for wisdom and compassion'
            }
        ],
        'unmotivated': [
            {
                'text': "A journey of a thousand miles begins with a single step.",
                'author': 'Lao Tzu',
                'theme': 'action',
                'application': 'Start with the smallest possible action today'
            },
            {
                'text': "The best time to plant a tree was 20 years ago. The second best time is now.",
                'author': 'Chinese Proverb',
                'theme': 'action',
                'application': 'Stop waiting for the perfect moment - begin now'
            }
        ],
        'stressed': [
            {
                'text': "You have been assigned this mountain to show others it can be moved.",
                'author': 'Mel Robbins',
                'theme': 'strength',
                'application': 'Your challenges are developing your strength for a purpose'
            }
        ]
    }
    
    # Get quotes for mood or default to general motivational quotes
    relevant_quotes = quotes_by_mood.get(mood, quotes_by_mood['unmotivated'])
    selected_quote = random.choice(relevant_quotes)
    
    # Add house-specific wisdom
    house_wisdom = get_house_wisdom_for_quote(selected_quote['theme'], house)
    
    return {
        'success': True,
        'type': 'curated',
        'quote': selected_quote['text'],
        'author': selected_quote['author'],
        'theme': selected_quote['theme'],
        'application': selected_quote['application'],
        'house_wisdom': house_wisdom,
        'mood': mood,
        'context': context,
        'house': house
    }

def get_daily_quote_collection() -> list:
    """Get collection of daily quotes"""
    return [
        {
            'text': 'It is our choices that show what we truly are, far more than our abilities.',
            'author': 'Albus Dumbledore',
            'theme': 'choice',
            'reflection': 'What choice will you make today that reflects your true character?'
        },
        {
            'text': 'Happiness can be found even in the darkest of times, if one only remembers to turn on the light.',
            'author': 'Albus Dumbledore', 
            'theme': 'hope',
            'reflection': 'What "light" can you turn on in your life today?'
        },
        {
            'text': 'We must all face the choice between what is right and what is easy.',
            'author': 'Albus Dumbledore',
            'theme': 'integrity',
            'reflection': 'Where in your life are you choosing the easy path over the right path?'
        },
        {
            'text': 'It takes great courage to stand up to our enemies, but even greater courage to stand up to our friends.',
            'author': 'Albus Dumbledore',
            'theme': 'courage',
            'reflection': 'When have you had to show courage in an unexpected way?'
        },
        {
            'text': 'The best of us must sometimes eat our words.',
            'author': 'Albus Dumbledore',
            'theme': 'humility',
            'reflection': 'What belief or position might you need to reconsider?'
        }
    ]

def get_house_style(house: str) -> str:
    """Get stylistic approach for each house"""
    styles = {
        'gryffindor': 'bold and inspiring',
        'hufflepuff': 'warm and encouraging',
        'ravenclaw': 'wise and thought-provoking',
        'slytherin': 'ambitious and strategic'
    }
    return styles.get(house.lower(), 'wise and encouraging')

def get_house_wisdom(theme: str) -> dict:
    """Get house-specific wisdom for a theme"""
    return {
        'gryffindor': f"A Gryffindor approaches {theme} with boldness and heart.",
        'hufflepuff': f"A Hufflepuff finds {theme} through patience and loyalty.",
        'ravenclaw': f"A Ravenclaw discovers {theme} through wisdom and learning.",
        'slytherin': f"A Slytherin achieves {theme} through determination and strategy."
    }

def get_house_wisdom_for_quote(theme: str, house: str) -> str:
    """Get specific house wisdom for a quote theme"""
    wisdom_map = {
        'gryffindor': {
            'courage': "True Gryffindor courage isn't the absence of fear - it's acting despite it.",
            'hope': "A Gryffindor's hope burns bright even in the darkest dungeons.",
            'action': "Gryffindors lead by example - be the change you want to see.",
            'strength': "Your strength comes not from your sword, but from your heart."
        },
        'hufflepuff': {
            'courage': "Hufflepuff courage is quiet but unwavering - like roots that hold the tree steady.",
            'hope': "Hope grows in Hufflepuff hearts like seedlings in rich soil - patient and sure.",
            'action': "Small, consistent actions create the most lasting change.",
            'strength': "True strength lies in lifting others as you climb."
        },
        'ravenclaw': {
            'courage': "Ravenclaw courage is the bravery to question, to learn, and to grow.",
            'hope': "Hope is the hypothesis that tomorrow can be better - test it daily.",
            'action': "Wise action comes from careful observation and thoughtful planning.",
            'strength': "Knowledge is power, but wisdom is knowing how to use it well."
        },
        'slytherin': {
            'courage': "Slytherin courage is strategic - knowing when to strike and when to wait.",
            'hope': "Hope without a plan is just a wish - make yours a strategy.",
            'action': "Every action should move you closer to your ultimate goal.",
            'strength': "True power comes from understanding yourself and your purpose."
        }
    }
    
    house_wisdom = wisdom_map.get(house.lower(), {})
    return house_wisdom.get(theme, f"Apply this wisdom in your own unique way.")

def get_quotes_by_theme(theme: str, limit: int) -> list:
    """Get quotes filtered by theme"""
    theme_quotes = {
        'courage': [
            {'text': 'Courage is not the absence of fear, but action in spite of it.', 'author': 'Mark Twain'},
            {'text': 'You are braver than you believe, stronger than you seem, and smarter than you think.', 'author': 'A.A. Milne'},
            {'text': 'The cave you fear to enter holds the treasure you seek.', 'author': 'Joseph Campbell'}
        ],
        'wisdom': [
            {'text': 'The only true wisdom is in knowing you know nothing.', 'author': 'Socrates'},
            {'text': 'Yesterday I was clever, so I wanted to change the world. Today I am wise, so I am changing myself.', 'author': 'Rumi'},
            {'text': 'The more that you read, the more things you will know. The more that you learn, the more places you\'ll go.', 'author': 'Dr. Seuss'}
        ],
        'perseverance': [
            {'text': 'It does not matter how slowly you go as long as you do not stop.', 'author': 'Confucius'},
            {'text': 'Success is not final, failure is not fatal: it is the courage to continue that counts.', 'author': 'Winston Churchill'},
            {'text': 'The difference between ordinary and extraordinary is that little extra.', 'author': 'Jimmy Johnson'}
        ]
    }
    
    quotes = theme_quotes.get(theme, theme_quotes['courage'])
    return quotes[:limit]

def get_theme_categories() -> dict:
    """Get available quote themes"""
    return {
        'courage': 'Quotes about bravery and facing fears',
        'wisdom': 'Quotes about learning and understanding',
        'perseverance': 'Quotes about persistence and resilience',
        'hope': 'Quotes about optimism and faith',
        'growth': 'Quotes about personal development',
        'leadership': 'Quotes about guiding and inspiring others',
        'friendship': 'Quotes about relationships and loyalty',
        'success': 'Quotes about achievement and goals'
    }

def create_custom_quote_prompt(situation: str, goal: str, challenge: str, style: str) -> str:
    """Create prompt for custom quote generation"""
    return f"""Create an original, inspiring quote for someone in this situation:

Situation: {situation}
Goal: {goal}
Challenge: {challenge}
Preferred style: {style}

The quote should be:
- Original and memorable
- Directly relevant to their situation
- Actionable and empowering
- Written in a {style} tone

Format: "Quote text" - Original Author (you can attribute it to a fictional wise character or leave it anonymous)

Also provide a brief explanation of how to apply this wisdom."""

def generate_template_quote(situation: str, goal: str, challenge: str, style: str) -> dict:
    """Generate quote using templates as fallback"""
    templates = {
        'inspiring': [
            f"Your {goal} is not just a dream—it's a promise you're making to your future self.",
            f"Every {challenge} you face is building the strength you need for your {goal}.",
            f"In the space between where you are and where you want to be lies all the magic."
        ],
        'practical': [
            f"The path to {goal} is walked one small step at a time, especially when facing {challenge}.",
            f"You don't have to be perfect at handling {challenge}—you just have to keep going toward {goal}.",
            f"Progress, not perfection, is what transforms {situation} into success."
        ],
        'philosophical': [
            f"Perhaps {challenge} is not an obstacle to {goal}, but the very thing that will make achieving it meaningful.",
            f"In every {situation}, there are seeds of the person you're becoming.",
            f"The universe places {challenge} on the path to {goal} not to stop you, but to prepare you."
        ]
    }
    
    style_templates = templates.get(style, templates['inspiring'])
    selected_quote = random.choice(style_templates)
    
    return {
        'success': True,
        'type': 'template_generated',
        'quote': selected_quote,
        'author': 'Mirror of Erised',
        'situation': situation,
        'goal': goal,
        'challenge': challenge,
        'style': style,
        'application': f"Remember this when {challenge} feels overwhelming - you're building toward {goal}."
    }

def generate_mirror_insight(situation: str, goal: str) -> str:
    """Generate insight from the Mirror of Erised"""
    insights = [
        f"The Mirror shows not what you lack, but what you already possess to transform {situation}.",
        f"Your desire for {goal} reveals the strength already growing within you.",
        f"What you seek in {goal} is calling forth qualities you didn't know you had.",
        f"The Mirror reflects not just your dreams, but your readiness to make them real."
    ]
    
    return random.choice(insights)

def generate_default_reflection_questions(quote: str) -> list:
    """Generate default reflection questions"""
    return [
        "How does this quote apply to your current situation?",
        "What would change if you truly believed this message?", 
        "What small action could you take today that embodies this wisdom?",
        "Who in your life exemplifies the truth of this quote?"
    ]

def generate_journaling_prompts(quote: str) -> list:
    """Generate journaling prompts based on quote"""
    return [
        f"Write about a time when you experienced the truth of: '{quote[:50]}...'",
        "What resistance do you feel to this message, and what might that reveal?",
        "How would your week look different if you lived by this quote?",
        "What would you tell a friend who needed to hear this message?"
    ]

def generate_action_suggestions(quote: str) -> list:
    """Generate actionable suggestions"""
    return [
        "Write this quote somewhere you'll see it daily",
        "Share this quote with someone who might need to hear it",
        "Identify one specific way to apply this wisdom today",
        "Set a reminder to reflect on this quote again next week"
    ]

def find_related_quotes(quote: str) -> list:
    """Find related quotes (simplified implementation)"""
    # In a real implementation, this would use semantic similarity
    return [
        "The best way out is always through. - Robert Frost",
        "What lies behind us and what lies before us are tiny matters compared to what lies within us. - Ralph Waldo Emerson",
        "You are never too old to set another goal or to dream a new dream. - C.S. Lewis"
    ]