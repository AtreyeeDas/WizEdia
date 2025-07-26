"""
Potion Mixer API - Concept Interaction Analysis
Analyzes how different concepts, emotions, or ideas interact when combined
"""

from flask import Blueprint, request, jsonify
from services.gemini_chat import gemini_chat
from services.hf_nlp import hf_nlp
from utils.verify_firebase import optional_auth
from utils.helpers import clean_text, safe_json_response

potion_bp = Blueprint('potion', __name__)

@potion_bp.route('/mix', methods=['POST'])
@optional_auth  
def mix_concepts():
    """Analyze interaction between two concepts/emotions/ideas"""
    try:
        data = request.get_json()
        
        if not data or 'text1' not in data or 'text2' not in data:
            return jsonify({'error': 'Two concepts are required for potion mixing'}), 400
        
        concept1 = clean_text(data['text1'])
        concept2 = clean_text(data['text2'])
        
        if not concept1 or not concept2:
            return jsonify({'error': 'Valid concept content is required for both ingredients'}), 400
        
        # Analyze individual concepts first
        analysis1 = analyze_concept(concept1)
        analysis2 = analyze_concept(concept2)
        
        # Generate interaction analysis
        interaction_prompt = create_interaction_prompt(concept1, concept2, analysis1, analysis2)
        
        # Get LLM analysis of the interaction
        interaction_response = gemini_chat.chat(
            prompt=interaction_prompt,
            context="You are a wise potion master analyzing the magical interaction between concepts.",
            personality='professor'
        )
        
        if not interaction_response['success']:
            return jsonify({
                'error': 'Potion mixing cauldron is temporarily unavailable',
                'fallback_result': get_fallback_interaction(concept1, concept2)
            }), 500
        
        # Determine interaction type and effects
        interaction_type = determine_interaction_type(concept1, concept2)
        stability_score = calculate_stability(analysis1, analysis2)
        
        response_data = {
            'success': True,
            'ingredient1': {
                'concept': concept1,
                'properties': analysis1
            },
            'ingredient2': {
                'concept': concept2,
                'properties': analysis2
            },
            'interaction': {
                'type': interaction_type,
                'description': interaction_response['response'],
                'stability_score': stability_score,
                'effects': generate_interaction_effects(interaction_type),
                'warnings': generate_warnings(stability_score),
                'suggestions': generate_improvement_suggestions(concept1, concept2, stability_score)
            },
            'potion_result': {
                'name': generate_potion_name(concept1, concept2),
                'color': get_potion_color(interaction_type),
                'magical_properties': get_magical_properties(interaction_type)
            }
        }
        
        # Add brewing history for authenticated users
        if hasattr(request, 'user') and request.user:
            response_data['user_id'] = request.user.get('uid')
            response_data['brewing_session'] = get_brewing_session_count(request.user.get('uid'))
        
        return safe_json_response(response_data)
        
    except Exception as e:
        return jsonify({
            'error': 'Potion mixing encountered an unexpected magical mishap',
            'details': str(e)
        }), 500

@potion_bp.route('/recipes', methods=['GET'])
def get_potion_recipes():
    """Get curated potion recipes for common concept combinations"""
    recipes = {
        'confidence_courage': {
            'ingredients': ['self-confidence', 'courage'],
            'result': 'Bravery Elixir',
            'description': 'A powerful combination that transforms self-doubt into bold action',
            'brewing_time': '21 days of practice',
            'side_effects': 'May cause increased willingness to take risks'
        },
        'anxiety_preparation': {
            'ingredients': ['anxiety', 'thorough preparation'],
            'result': 'Focused Clarity Potion',
            'description': 'Channels nervous energy into productive preparation',
            'brewing_time': '1-2 weeks of structured study',
            'side_effects': 'Temporary perfectionist tendencies'
        },
        'creativity_discipline': {
            'ingredients': ['creative thinking', 'discipline'],
            'result': 'Innovation Brew',
            'description': 'Balances free-flowing ideas with structured execution',
            'brewing_time': '30 days of consistent practice',
            'side_effects': 'Increased productivity and breakthrough insights'
        },
        'failure_growth': {
            'ingredients': ['failure experience', 'growth mindset'],
            'result': 'Phoenix Potion',
            'description': 'Transforms setbacks into stepping stones for success',
            'brewing_time': '3-6 months of reflection and action',
            'side_effects': 'Enhanced resilience and wisdom'
        }
    }
    
    return jsonify({
        'success': True,
        'recipes': recipes,
        'brewing_tips': [
            'Start with small doses and gradually increase',
            'Always combine opposing forces slowly',
            'Monitor emotional temperature during brewing',
            'Document your brewing process for future reference'
        ]
    })

@potion_bp.route('/analyze-batch', methods=['POST'])
@optional_auth
def analyze_concept_batch():
    """Analyze multiple concepts and their collective interaction"""
    try:
        data = request.get_json()
        
        if not data or 'concepts' not in data:
            return jsonify({'error': 'List of concepts is required for batch analysis'}), 400
        
        concepts = [clean_text(concept) for concept in data['concepts']]
        concepts = [c for c in concepts if c]  # Remove empty concepts
        
        if len(concepts) < 2:
            return jsonify({'error': 'At least 2 valid concepts are required'}), 400
        
        if len(concepts) > 5:
            return jsonify({'error': 'Maximum 5 concepts allowed per batch'}), 400
        
        # Analyze each concept
        concept_analyses = {}
        for concept in concepts:
            concept_analyses[concept] = analyze_concept(concept)
        
        # Generate batch interaction analysis
        batch_prompt = create_batch_interaction_prompt(concepts, concept_analyses)
        
        batch_response = gemini_chat.chat(
            prompt=batch_prompt,
            context="You are analyzing a complex potion with multiple ingredients.",
            personality='professor'
        )
        
        # Calculate overall harmony and stability
        harmony_score = calculate_batch_harmony(concept_analyses)
        dominant_trait = find_dominant_trait(concept_analyses)
        
        response_data = {
            'success': True,
            'concepts': concepts,
            'individual_analyses': concept_analyses,
            'batch_analysis': {
                'description': batch_response['response'] if batch_response['success'] else 'Complex interaction requiring careful balance',
                'harmony_score': harmony_score,
                'dominant_trait': dominant_trait,
                'overall_effect': determine_overall_effect(harmony_score),
                'brewing_difficulty': get_brewing_difficulty(len(concepts), harmony_score),
                'recommended_order': suggest_brewing_order(concepts, concept_analyses)
            }
        }
        
        return safe_json_response(response_data)
        
    except Exception as e:
        return jsonify({
            'error': 'Batch analysis failed',
            'details': str(e)
        }), 500

def analyze_concept(concept: str) -> dict:
    """Analyze individual concept properties"""
    # Basic concept analysis (could be enhanced with NLP)
    concept_lower = concept.lower()
    
    # Determine emotional valence
    positive_words = ['joy', 'confidence', 'success', 'love', 'hope', 'courage']
    negative_words = ['fear', 'anxiety', 'failure', 'anger', 'sadness', 'doubt']
    
    valence = 'neutral'
    if any(word in concept_lower for word in positive_words):
        valence = 'positive'
    elif any(word in concept_lower for word in negative_words):
        valence = 'negative'
    
    # Determine energy level
    high_energy_words = ['excitement', 'anger', 'passion', 'enthusiasm']
    low_energy_words = ['calm', 'peace', 'sadness', 'depression']
    
    energy = 'medium'
    if any(word in concept_lower for word in high_energy_words):
        energy = 'high'
    elif any(word in concept_lower for word in low_energy_words):
        energy = 'low'
    
    return {
        'valence': valence,
        'energy': energy,
        'complexity': len(concept.split()),
        'category': categorize_concept(concept)
    }

def categorize_concept(concept: str) -> str:
    """Categorize concept into type"""
    concept_lower = concept.lower()
    
    emotion_words = ['happy', 'sad', 'angry', 'fear', 'joy', 'anxiety']
    skill_words = ['programming', 'writing', 'mathematics', 'communication']
    trait_words = ['confidence', 'courage', 'patience', 'discipline']
    
    if any(word in concept_lower for word in emotion_words):
        return 'emotion'
    elif any(word in concept_lower for word in skill_words):
        return 'skill'
    elif any(word in concept_lower for word in trait_words):
        return 'trait'
    else:
        return 'abstract'

def create_interaction_prompt(concept1: str, concept2: str, analysis1: dict, analysis2: dict) -> str:
    """Create prompt for analyzing concept interaction"""
    return f"""Analyze the interaction between "{concept1}" and "{concept2}".

Concept 1 properties: {analysis1}
Concept 2 properties: {analysis2}

Consider:
1. How do these concepts complement or conflict with each other?
2. What happens when they're combined in someone's experience?
3. What are the potential positive and negative outcomes?
4. How can this combination be optimized for the best results?

Provide a detailed but accessible analysis."""

def determine_interaction_type(concept1: str, concept2: str) -> str:
    """Determine the type of interaction between concepts"""
    # This is a simplified version - could be enhanced with ML
    opposing_pairs = [
        ('confidence', 'anxiety'), ('success', 'failure'), ('hope', 'despair'),
        ('courage', 'fear'), ('calm', 'chaos'), ('order', 'disorder')
    ]
    
    c1_lower = concept1.lower()
    c2_lower = concept2.lower()
    
    for pair in opposing_pairs:
        if (pair[0] in c1_lower and pair[1] in c2_lower) or (pair[1] in c1_lower and pair[0] in c2_lower):
            return 'transformative'
    
    # Check for complementary concepts
    complementary_indicators = ['and', 'with', 'plus']
    if any(indicator in f"{c1_lower} {c2_lower}" for indicator in complementary_indicators):
        return 'synergistic'
    
    return 'neutral'

def calculate_stability(analysis1: dict, analysis2: dict) -> float:
    """Calculate stability score of concept interaction"""
    stability = 0.5  # Base stability
    
    # Same valence increases stability
    if analysis1['valence'] == analysis2['valence']:
        stability += 0.2
    elif analysis1['valence'] != 'neutral' and analysis2['valence'] != 'neutral':
        stability -= 0.1  # Opposing valences create instability
    
    # Similar energy levels increase stability
    if analysis1['energy'] == analysis2['energy']:
        stability += 0.15
    
    # Complexity affects stability
    total_complexity = analysis1['complexity'] + analysis2['complexity']
    if total_complexity > 4:
        stability -= 0.1
    
    return max(0.0, min(1.0, stability))

def generate_interaction_effects(interaction_type: str) -> list:
    """Generate effects based on interaction type"""
    effects_by_type = {
        'synergistic': [
            'Amplified positive outcomes',
            'Increased overall effectiveness', 
            'Enhanced problem-solving ability'
        ],
        'transformative': [
            'Potential for significant personal growth',
            'Initial instability followed by breakthrough',
            'Radical shift in perspective possible'
        ],
        'neutral': [
            'Gradual steady progress',
            'Balanced but moderate effects',
            'Safe but limited transformation'
        ]
    }
    
    return effects_by_type.get(interaction_type, ['Unknown interaction pattern'])

def generate_warnings(stability_score: float) -> list:
    """Generate warnings based on stability"""
    if stability_score < 0.3:
        return [
            'High volatility - proceed with caution',
            'May cause emotional turbulence initially',
            'Requires careful monitoring and adjustment'
        ]
    elif stability_score < 0.6:
        return [
            'Moderate stability - some fluctuation expected',
            'Benefits may take time to manifest'
        ]
    else:
        return ['Stable interaction - generally safe to proceed']

def generate_improvement_suggestions(concept1: str, concept2: str, stability: float) -> list:
    """Generate suggestions for improving the interaction"""
    suggestions = []
    
    if stability < 0.5:
        suggestions.extend([
            f'Consider gradual introduction of {concept2} while maintaining {concept1}',
            'Add stabilizing practices like reflection or mindfulness',
            'Monitor emotional responses closely during the process'
        ])
    
    suggestions.extend([
        'Practice combining these concepts in low-stakes situations first',
        'Journal about your experiences with this combination',
        'Seek guidance from mentors who embody both qualities'
    ])
    
    return suggestions

def generate_potion_name(concept1: str, concept2: str) -> str:
    """Generate a creative name for the concept combination"""
    name_templates = [
        f"Elixir of {concept1.title()} and {concept2.title()}",
        f"{concept1.title()}-{concept2.title()} Brew",
        f"The {concept1.title()} {concept2.title()} Potion",
        f"Essence of Combined {concept1.title()}"
    ]
    
    return name_templates[hash(concept1 + concept2) % len(name_templates)]

def get_potion_color(interaction_type: str) -> str:
    """Get potion color based on interaction type"""
    colors = {
        'synergistic': 'Golden with silver swirls',
        'transformative': 'Deep purple shifting to bright blue', 
        'neutral': 'Steady emerald green'
    }
    
    return colors.get(interaction_type, 'Mysterious opalescent')

def get_magical_properties(interaction_type: str) -> list:
    """Get magical properties of the resulting potion"""
    properties = {
        'synergistic': [
            'Enhances natural abilities',
            'Increases harmony between different life areas',
            'Provides sustained energy boost'
        ],
        'transformative': [
            'Catalyzes deep personal change',
            'Breaks through limiting patterns',
            'Reveals hidden potential'
        ],
        'neutral': [
            'Provides gentle support',
            'Maintains emotional balance',
            'Offers steady progress'
        ]
    }
    
    return properties.get(interaction_type, ['Unknown magical effects'])

def get_brewing_session_count(user_id: str) -> int:
    """Get user's brewing session count (mock)"""
    return 15  # Mock data

def get_fallback_interaction(concept1: str, concept2: str) -> dict:
    """Provide fallback interaction analysis"""
    return {
        'type': 'neutral',
        'description': f'The combination of {concept1} and {concept2} creates an interesting dynamic that requires careful observation. Each person experiences this combination differently based on their unique circumstances.',
        'stability_score': 0.5,
        'effects': ['Individual results may vary', 'Requires personal experimentation'],
        'warnings': ['Monitor your own response to this combination'],
        'suggestions': ['Start slowly and adjust based on your experience']
    }

def create_batch_interaction_prompt(concepts: list, analyses: dict) -> str:
    """Create prompt for batch concept analysis"""
    concept_list = ', '.join(concepts)
    return f"""Analyze the complex interaction between multiple concepts: {concept_list}.

Individual concept properties:
{analyses}

Consider:
1. How do all these concepts work together as a system?
2. Which concepts dominate or get overshadowed?
3. What emergent properties arise from this combination?
4. What's the overall trajectory of someone embodying all these concepts?

Provide insights on managing this complex combination."""

def calculate_batch_harmony(analyses: dict) -> float:
    """Calculate harmony score for multiple concepts"""
    if len(analyses) < 2:
        return 1.0
    
    valences = [info['valence'] for info in analyses.values()]
    energies = [info['energy'] for info in analyses.values()]
    
    # Check valence harmony
    positive_count = valences.count('positive')
    negative_count = valences.count('negative')
    neutral_count = valences.count('neutral')
    
    valence_harmony = 1.0 - abs(positive_count - negative_count) / len(valences)
    
    # Check energy harmony  
    high_count = energies.count('high')
    low_count = energies.count('low')
    medium_count = energies.count('medium')
    
    energy_harmony = 1.0 - abs(high_count - low_count) / len(energies)
    
    return (valence_harmony + energy_harmony) / 2

def find_dominant_trait(analyses: dict) -> str:
    """Find the dominant trait in a batch"""
    categories = [info['category'] for info in analyses.values()]
    category_counts = {cat: categories.count(cat) for cat in set(categories)}
    
    return max(category_counts, key=category_counts.get)

def determine_overall_effect(harmony_score: float) -> str:
    """Determine overall effect based on harmony"""
    if harmony_score > 0.8:
        return 'Highly harmonious - concepts work together beautifully'
    elif harmony_score > 0.6:
        return 'Generally harmonious - minor tensions but overall positive'
    elif harmony_score > 0.4:
        return 'Moderately complex - requires active management'
    else:
        return 'Highly complex - significant effort needed to balance'

def get_brewing_difficulty(concept_count: int, harmony: float) -> str:
    """Determine brewing difficulty"""
    base_difficulty = concept_count - 2  # 2 concepts = 0 additional difficulty
    harmony_penalty = (1 - harmony) * 2
    
    total_difficulty = base_difficulty + harmony_penalty
    
    if total_difficulty < 1:
        return 'Beginner'
    elif total_difficulty < 2:
        return 'Intermediate'
    elif total_difficulty < 3:
        return 'Advanced'
    else:
        return 'Master Level'

def suggest_brewing_order(concepts: list, analyses: dict) -> list:
    """Suggest order for introducing concepts"""
    # Sort by stability (positive valence and medium energy first)
    def stability_score(concept):
        info = analyses[concept]
        score = 0
        if info['valence'] == 'positive':
            score += 2
        elif info['valence'] == 'neutral':
            score += 1
        
        if info['energy'] == 'medium':
            score += 2
        elif info['energy'] in ['high', 'low']:
            score += 1
        
        score -= info['complexity']  # Lower complexity first
        return score
    
    return sorted(concepts, key=stability_score, reverse=True)