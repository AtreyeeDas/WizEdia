"""
Forbidden Library API - Content Analysis and Ethics
Summarizes content and performs ethics checking on texts, PDFs, and URLs
"""

from flask import Blueprint, request, jsonify
from services.gemini_chat import gemini_chat
from services.hf_nlp import hf_nlp
from utils.verify_firebase import optional_auth
from utils.helpers import clean_text, safe_json_response, extract_keywords
import requests
import re

library_bp = Blueprint('library', __name__)

@library_bp.route('/summarize', methods=['POST'])
@optional_auth
def summarize_content():
    """Summarize content and perform ethics analysis"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'Content data is required'}), 400
        
        # Get content from various sources
        content_text = ""
        content_source = ""
        
        if 'text' in data:
            content_text = clean_text(data['text'])
            content_source = "direct_text"
        elif 'url' in data:
            url_result = extract_content_from_url(data['url'])
            if url_result['success']:
                content_text = url_result['content']
                content_source = f"url: {data['url']}"
            else:
                return jsonify({
                    'error': 'Failed to extract content from URL',
                    'details': url_result.get('error', 'Unknown error')
                }), 400
        else:
            return jsonify({'error': 'Either text or url is required'}), 400
        
        if not content_text:
            return jsonify({'error': 'No valid content found to analyze'}), 400
        
        # Limit content length for processing
        if len(content_text) > 10000:
            content_text = content_text[:10000] + "..."
        
        # Generate summary
        summary_result = generate_content_summary(content_text)
        
        # Perform ethics analysis
        ethics_result = analyze_content_ethics(content_text)
        
        # Extract key themes and concepts
        themes = extract_content_themes(content_text)
        
        response_data = {
            'success': True,
            'content_source': content_source,
            'content_length': len(content_text),
            'summary': summary_result,
            'ethics_analysis': ethics_result,
            'themes': themes,
            'content_classification': categorize_content(content_text),
        }
        
        return safe_json_response(response_data)
        
    except Exception as e:
        return jsonify({
            'error': 'Content analysis encountered an unexpected error',
            'details': str(e)
        }), 500

@library_bp.route('/fact-check', methods=['POST'])
@optional_auth
def fact_check_content():
    """Perform fact-checking and source verification on content"""
    try:
        data = request.get_json()
        
        if not data or 'text' not in data:
            return jsonify({'error': 'Text content is required for fact-checking'}), 400
        
        text = clean_text(data['text'])
        
        if not text:
            return jsonify({'error': 'Valid text content is required'}), 400
        
        # Extract claims from the text
        claims = extract_claims(text)
        
        # Analyze credibility indicators
        credibility_analysis = analyze_credibility_indicators(text)
        
        # Check for bias indicators
        bias_analysis = analyze_bias_indicators(text)
               
        response_data = {
            'success': True,
            'extracted_claims': claims,
            'credibility_analysis': credibility_analysis,
            'bias_analysis': bias_analysis,
            'overall_reliability_score': calculate_reliability_score(credibility_analysis, bias_analysis)
        }
        
        return safe_json_response(response_data)
        
    except Exception as e:
        return jsonify({
            'error': 'Fact-checking analysis failed',
            'details': str(e)
        }), 500

@library_bp.route('/compare-sources', methods=['POST'])
@optional_auth
def compare_sources():
    """Compare multiple sources on the same topic"""
    try:
        data = request.get_json()
        
        if not data or 'sources' not in data:
            return jsonify({'error': 'List of sources is required'}), 400
        
        sources = data['sources']
        
        # Analyze each source
        source_analyses = []
        for i, source in enumerate(sources):
            source_text = clean_text(source.get('text', ''))
            if source_text:
                analysis = {
                    'source_id': i + 1,
                    'title': source.get('title', f'Source {i + 1}'),
                    'url': source.get('url', ''),
                    'themes': extract_content_themes(source_text),
                    'summary': generate_content_summary(source_text),
                    'credibility': analyze_credibility_indicators(source_text),
                    'bias': analyze_bias_indicators(source_text)
                }
                source_analyses.append(analysis)
        
        if not source_analyses:
            return jsonify({'error': 'No valid source content found'}), 400
        source_analyses.append({'success': True})
        
        return safe_json_response(source_analyses)
        
    except Exception as e:
        return jsonify({
            'error': 'Source comparison failed',
            'details': str(e)
        }), 500

@library_bp.route('/research-assistant', methods=['POST'])
@optional_auth
def research_assistant():
    """Provide research guidance and methodology suggestions"""
    try:
        data = request.get_json()
        
        if not data or 'topic' not in data:
            return jsonify({'error': 'Research topic is required'}), 400
        
        topic = clean_text(data['topic'])
        research_level = data.get('level', 'undergraduate')  # undergraduate, graduate, professional
        research_type = data.get('type', 'general')  # general, literature_review, empirical, theoretical
        
        if not topic:
            return jsonify({'error': 'Valid research topic is required'}), 400
        
        # Suggest research sources
        research_sources = suggest_research_sources(topic, research_level)
        
        # Provide methodology guidance
        methodology_guidance = provide_methodology_guidance(topic, research_type)
        
        # Generate research questions
        research_questions = generate_research_questions(topic, research_level)
        
        # Create research timeline
        research_timeline = create_research_timeline(research_level, research_type)
        
        response_data = {
            'success': True,
            'topic': topic,
            'research_level': research_level,
            'research_type': research_type,
            'recommended_sources': research_sources,
            'methodology_guidance': methodology_guidance,
            'suggested_research_questions': research_questions,
            'research_timeline': research_timeline,
            'ethical_considerations': get_research_ethics_guidelines(research_type)
        }
        
        return safe_json_response(response_data)
        
    except Exception as e:
        return jsonify({
            'error': 'Research assistance failed',
            'details': str(e)
        }), 500

@library_bp.route('/plagiarism-checker', methods=['POST'])
@optional_auth
def citation_helper():
    #Help check plagiarism
    try:
        data = request.get_json()
        
        if not data or 'text' not in data:
            return jsonify({'error': 'Content data is required'}), 400
        
        # Get content from various sources
        content_text = clean_text(data['text'])
        if not content_text:
            return jsonify({'error': 'Valid content text is required'}), 400
        plagiarism_prompt = f"""Check the following text extracted from a research paper thoroughly for plagiarism:
                        Text: {content_text[:3000]}...
        If possible,
        Provide List of paper citations in APA or Harvard Style(2-3 sentences) from which the content may be plagiarised.
        Be specific and accurate, as if you are a plagiarism expert.
        If no plagiarism is found, return "No plagiarism detected"."""
        plag_response = gemini_chat.chat(
            prompt=content_text,
            context="You are a plagiarism checker for research papers.",
            personality='professor'
        )
        if plag_response['success']:
            return jsonify({
                'success': True,
                'plagiarism_text': plag_response["response"],
                'plagiarism_method': 'llm_generated'
            })
        if not plag_response['success']:
            return jsonify({
                'error': 'Plagiarism checker is temporarily unavailable',
            }), 500
    except Exception as e:
        return jsonify({
            'error': 'Plagiarism checker failed',
            'details': str(e)
        }), 500
   

def extract_content_from_url(url: str) -> dict:
    """Extract text content from URL"""
    try:
        # Basic URL validation
        if not url.startswith(('http://', 'https://')):
            return {'success': False, 'error': 'Invalid URL format'}
        
        # Simple content extraction (in real implementation, use libraries like BeautifulSoup)
        response = requests.get(url, timeout=10, headers={
            'User-Agent': 'Mozilla/5.0 (WizEdia Content Analyzer)'
        })
        
        if response.status_code == 200:
            # Very basic text extraction (remove HTML tags)
            content = re.sub(r'<[^>]+>', '', response.text)
            content = re.sub(r'\s+', ' ', content).strip()
            
            # Limit content length
            if len(content) > 8000:
                content = content[:8000]
            
            return {
                'success': True,
                'content': content,
                'url': url,
                'content_length': len(content)
            }
        else:
            return {
                'success': False,
                'error': f'Failed to fetch URL: {response.status_code}'
            }
            
    except Exception as e:
        return {
            'success': False,
            'error': f'URL extraction error: {str(e)}'
        }

def generate_content_summary(text: str) -> dict:
    """Generate comprehensive summary of content"""
    try:
        # Use LLM for summarization
        summary_prompt = f"""Summarize the following text in a clear, concise manner:

Text: {text[:3000]}...

Provide:
1. A brief summary (2-3 sentences)
2. Key points (3-5 bullet points)

Focus on the most important information and insights."""
        
        summary_response = gemini_chat.chat(
            prompt=summary_prompt,
            context="You are a skilled academic summarizer helping students understand complex content.",
            personality='professor'
        )
        
        if summary_response['success']:
            return {
                'success': True,
                'summary_text': summary_response['response'],
                'word_count': len(text.split()),
                'summary_method': 'llm_generated'
            }
        else:
            # Fallback to extractive summary
            return generate_extractive_summary(text)
            
    except Exception as e:
        return {
            'success': False,
            'error': f'Summary generation failed: {str(e)}',
            'fallback_summary': text[:500] + "..." if len(text) > 500 else text
        }

def generate_extractive_summary(text: str) -> dict:
    """Generate extractive summary as fallback"""
    sentences = text.split('.')
    
    # Simple extractive approach: take first few sentences and some from middle/end
    important_sentences = []
    
    if len(sentences) > 3:
        important_sentences.extend(sentences[:2])  # First 2 sentences
        
        if len(sentences) > 10:
            # Add some middle sentences
            middle_idx = len(sentences) // 2
            important_sentences.append(sentences[middle_idx])
        
        if len(sentences) > 5:
            # Add conclusion sentence
            important_sentences.append(sentences[-2])
    else:
        important_sentences = sentences
    
    summary = '. '.join(important_sentences).strip()
    
    return {
        'success': True,
        'summary_text': summary,
        'word_count': len(text.split()),
        'summary_method': 'extractive'
    }

def analyze_content_ethics(text: str) -> dict:
    """Analyze content for ethical considerations"""
    ethics_score = 0.7  # Base neutral score
    concerns = []
    positive_indicators = []
    
    text_lower = text.lower()
    
    # Check for concerning content
    concerning_keywords = [
        'discriminat', 'bias', 'stereotype', 'prejudice', 'misleading',
        'false', 'unverified', 'conspiracy', 'hate', 'harmful'
    ]
    
    for keyword in concerning_keywords:
        if keyword in text_lower:
            ethics_score -= 0.1
            concerns.append(f'Contains potentially {keyword} content')
    
    # Check for positive indicators
    positive_keywords = [
        'evidence', 'research', 'study', 'peer-reviewed', 'citation',
        'source', 'methodology', 'objective', 'balanced', 'factual'
    ]
    
    for keyword in positive_keywords:
        if keyword in text_lower:
            ethics_score += 0.05
            positive_indicators.append(f'Contains {keyword} indicators')
    
    # Ensure score stays within bounds
    ethics_score = max(0.0, min(1.0, ethics_score))
    
    return {
        'ethics_score': round(ethics_score, 2),
        'level': get_ethics_level(ethics_score),
        'concerns': concerns[:5],  # Limit to 5 concerns
        'positive_indicators': positive_indicators[:5],
        'recommendations': get_ethics_recommendations(ethics_score, concerns)
    }

def get_ethics_level(score: float) -> str:
    """Get ethics level description"""
    if score >= 0.8:
        return 'high_integrity'
    elif score >= 0.6:
        return 'generally_trustworthy'
    elif score >= 0.4:
        return 'requires_verification'
    else:
        return 'significant_concerns'

def get_ethics_recommendations(score: float, concerns: list) -> list:
    """Get ethics-based recommendations"""
    recommendations = []
    
    if score < 0.5:
        recommendations.append('Verify information with multiple independent sources')
        recommendations.append('Look for peer-reviewed or authoritative sources')
    
    if concerns:
        recommendations.append('Exercise critical thinking when evaluating claims')
        recommendations.append('Consider potential bias or agenda of the source')
    
    if score > 0.7:
        recommendations.append('Content appears reliable but always cross-reference important facts')
    
    recommendations.append('Practice information literacy skills when consuming content')
    
    return recommendations

def extract_content_themes(text: str) -> dict:
    """Extract main themes and topics from content"""
    # Extract keywords
    keywords = extract_keywords(text, max_keywords=10)
    
    # Categorize content
    categories = categorize_content(text)
    
    # Identify academic disciplines
    disciplines = identify_academic_disciplines(text)
    
    return {
        'primary_keywords': keywords[:5],
        'secondary_keywords': keywords[5:],
        'content_categories': categories,
        'academic_disciplines': disciplines,
        'complexity_level': assess_content_complexity(text)
    }

def categorize_content(text: str) -> list:
    """Categorize content into general categories"""
    text_lower = text.lower()
    categories = []
    
    category_keywords = {
        'scientific': ['research', 'study', 'experiment', 'hypothesis', 'methodology', 'analysis'],
        'historical': ['history', 'century', 'historical', 'past', 'era', 'period'],
        'technical': ['technology', 'software', 'programming', 'technical', 'system', 'algorithm'],
        'philosophical': ['philosophy', 'ethics', 'moral', 'philosophical', 'theory', 'concept'],
        'educational': ['education', 'learning', 'teaching', 'student', 'academic', 'curriculum'],
        'business': ['business', 'market', 'economic', 'financial', 'commercial', 'industry']
    }
    
    for category, keywords in category_keywords.items():
        if any(keyword in text_lower for keyword in keywords):
            categories.append(category)
    
    return categories if categories else ['general']

def identify_academic_disciplines(text: str) -> list:
    """Identify relevant academic disciplines"""
    text_lower = text.lower()
    disciplines = []
    
    discipline_keywords = {
        'computer_science': ['programming', 'algorithm', 'software', 'computing', 'code','machine learning'],
        'biology': ['biology', 'organism', 'cell', 'gene', 'evolution', 'ecology'],
        'physics': ['physics', 'quantum', 'energy', 'force', 'particle', 'relativity'],
        'chemistry': ['chemistry', 'molecule', 'reaction', 'compound', 'element'],
        'psychology': ['psychology', 'behavior', 'cognitive', 'mental', 'brain'],
        'mathematics': ['mathematics', 'equation', 'theorem', 'proof', 'calculation'],
        'history': ['history', 'historical', 'war', 'civilization', 'culture'],
        'literature': ['literature', 'poetry', 'novel', 'author', 'literary'],
        'economics': ['economics', 'market', 'trade', 'economic', 'finance'],
        'philosophy': ['philosophy', 'ethics', 'philosophical', 'moral', 'logic']
    }
    
    for discipline, keywords in discipline_keywords.items():
        keyword_count = sum(1 for keyword in keywords if keyword in text_lower)
        if keyword_count >= 2:  # Require at least 2 keywords for discipline match
            disciplines.append(discipline.replace('_', ' ').title())
    
    return disciplines

def assess_content_complexity(text: str) -> str:
    """Assess the complexity level of content"""
    # Simple complexity assessment based on various factors
    sentences = text.split('.')
    words = text.split()
    
    avg_sentence_length = len(words) / len(sentences) if sentences else 0
    
    # Count complex words (more than 6 characters)
    complex_words = [word for word in words if len(word) > 6]
    complexity_ratio = len(complex_words) / len(words) if words else 0
    
    # Technical terminology indicators
    technical_indicators = [
        'methodology', 'analysis', 'hypothesis', 'theoretical', 'empirical',
        'quantitative', 'qualitative', 'systematic', 'comprehensive'
    ]
    
    technical_count = sum(1 for term in technical_indicators if term in text.lower())
    
    # Determine complexity level
    complexity_score = (avg_sentence_length / 20) + complexity_ratio + (technical_count / 10)
    
    if complexity_score > 1.5:
        return 'advanced'
    elif complexity_score > 0.8:
        return 'intermediate'
    else:
        return 'beginner'

def extract_key_insights(text: str) -> list:
    """Extract key insights from content"""
    # Simple insight extraction based on sentence patterns
    sentences = text.split('.')
    insights = []
    
    insight_indicators = [
        'important', 'key', 'significant', 'crucial', 'essential',
        'conclusion', 'result', 'finding', 'discovery', 'reveals'
    ]
    
    for sentence in sentences:
        sentence = sentence.strip()
        if any(indicator in sentence.lower() for indicator in insight_indicators):
            if len(sentence) > 20 and len(sentence) < 200:  # Good length for insights
                insights.append(sentence)
    
    return insights[:5]  # Limit to 5 insights

def extract_claims(text: str) -> list:
    """Extract factual claims from text"""
    # Simple claim extraction based on sentence patterns
    sentences = text.split('.')
    claims = []
    
    claim_indicators = [
        'research shows', 'studies indicate', 'evidence suggests',
        'data reveals', 'according to', 'statistics show',
        'experts believe', 'scientists found'
    ]
    
    for sentence in sentences:
        sentence = sentence.strip()
        if any(indicator in sentence.lower() for indicator in claim_indicators):
            claims.append(sentence)
    
    # Also look for definitive statements
    definitive_patterns = ['is', 'are', 'will', 'must', 'always', 'never']
    for sentence in sentences:
        sentence = sentence.strip()
        if any(pattern in sentence.lower() for pattern in definitive_patterns):
            if len(sentence) > 30:  # Avoid very short sentences
                claims.append(sentence)
    
    return claims[:8]  # Limit to 8 claims

def analyze_credibility_indicators(text: str) -> dict:
    """Analyze indicators of content credibility"""
    credibility_score = 0.5  # Base score
    positive_indicators = []
    negative_indicators = []
    
    text_lower = text.lower()
    
    # Positive credibility indicators
    positive_keywords = [
        'peer-reviewed', 'citation', 'reference', 'bibliography',
        'methodology', 'data', 'evidence', 'research', 'study',
        'university', 'journal', 'published', 'verified'
    ]
    
    for keyword in positive_keywords:
        if keyword in text_lower:
            credibility_score += 0.05
            positive_indicators.append(keyword)
    
    # Negative credibility indicators
    negative_keywords = [
        'unverified', 'rumor', 'alleged', 'conspiracy',
        'secret', 'hidden truth', 'they don\'t want you to know',
        'shocking', 'amazing discovery', 'miracle'
    ]
    
    for keyword in negative_keywords:
        if keyword in text_lower:
            credibility_score -= 0.1
            negative_indicators.append(keyword)
    
    # Ensure score stays within bounds
    credibility_score = max(0.0, min(1.0, credibility_score))
    
    return {
        'credibility_score': round(credibility_score, 2),
        'level': get_credibility_level(credibility_score),
        'positive_indicators': positive_indicators[:5],
        'negative_indicators': negative_indicators[:5],
        'source_quality_assessment': assess_source_quality(text)
    }

def get_credibility_level(score: float) -> str:
    """Get credibility level description"""
    if score >= 0.8:
        return 'highly_credible'
    elif score >= 0.6:
        return 'credible'
    elif score >= 0.4:
        return 'questionable'
    else:
        return 'low_credibility'

def assess_source_quality(text: str) -> dict:
    """Assess quality indicators of the source"""
    return {
        'has_citations': 'citation' in text.lower() or 'reference' in text.lower(),
        'academic_language': 'methodology' in text.lower() or 'hypothesis' in text.lower(),
        'balanced_perspective': assess_balance(text),
        'recent_information': 'recent' in text.lower() or '2023' in text or '2024' in text
    }

def assess_balance(text: str) -> bool:
    """Assess if content presents balanced perspective"""
    # Simple balance assessment
    balance_indicators = [
        'however', 'although', 'while', 'nevertheless',
        'on the other hand', 'alternatively', 'conversely'
    ]
    
    return any(indicator in text.lower() for indicator in balance_indicators)

def analyze_bias_indicators(text: str) -> dict:
    """Analyze potential bias in content"""
    bias_score = 0.5  # Neutral starting point
    bias_indicators = []
    
    text_lower = text.lower()
    
    # Emotional language indicators
    emotional_words = [
        'amazing', 'shocking', 'unbelievable', 'incredible',
        'devastating', 'terrible', 'wonderful', 'perfect'
    ]
    
    emotional_count = sum(1 for word in emotional_words if word in text_lower)
    if emotional_count > 3:
        bias_score += 0.2
        bias_indicators.append('High emotional language')
    
    # Absolute statements
    absolute_words = ['always', 'never', 'all', 'none', 'every', 'completely']
    absolute_count = sum(1 for word in absolute_words if word in text_lower)
    if absolute_count > 2:
        bias_score += 0.15
        bias_indicators.append('Frequent absolute statements')
    
    # One-sided presentation
    if not assess_balance(text):
        bias_score += 0.1
        bias_indicators.append('Potentially one-sided presentation')
    
    return {
        'bias_score': round(min(1.0, bias_score), 2),
        'level': get_bias_level(bias_score),
        'indicators': bias_indicators,
        'recommendations': get_bias_recommendations(bias_score)
    }

def get_bias_level(score: float) -> str:
    """Get bias level description"""
    if score >= 0.8:
        return 'high_bias'
    elif score >= 0.6:
        return 'moderate_bias'
    else:
        return 'low_bias'

def get_bias_recommendations(score: float) -> list:
    """Get recommendations based on bias level"""
    if score >= 0.7:
        return [
            'Seek multiple perspectives on this topic',
            'Look for more neutral, academic sources',
            'Be aware of potential bias when interpreting information'
        ]
    else:
        return [
            'Content appears relatively balanced',
            'Still verify important facts with additional sources'
        ]

def generate_fact_check_recommendations(claims: list, credibility: dict) -> list:
    """Generate fact-checking recommendations"""
    recommendations = []
    
    if len(claims) > 5:
        recommendations.append('Many claims present - prioritize verifying the most important ones')
    
    if credibility['credibility_score'] < 0.6:
        recommendations.append('Low credibility indicators - verify all major claims')
    
    recommendations.extend([
        'Check claims against authoritative sources like academic journals',
        'Use fact-checking websites for controversial claims',
        'Look for original sources of cited statistics or studies',
        'Be especially cautious with claims that seem too good/bad to be true'
    ])
    
    return recommendations

def suggest_verification_sources(claims: list) -> list:
    """Suggest sources for verifying claims"""
    return [
        'Google Scholar for academic research',
        'Government databases and statistics',
        'Fact-checking websites (Snopes, FactCheck.org)',
        'Peer-reviewed journals in relevant fields',
        'Primary sources when available',
        'Multiple independent news sources'
    ]

def calculate_reliability_score(credibility: dict, bias: dict) -> dict:
    """Calculate overall reliability score"""
    credibility_score = credibility['credibility_score']
    bias_score = bias['bias_score']
    
    # Lower bias score is better, so invert it
    adjusted_bias = 1.0 - bias_score
    
    # Weighted average (credibility weighted more heavily)
    reliability = (credibility_score * 0.7) + (adjusted_bias * 0.3)
    
    return {
        'score': round(reliability, 2),
        'level': get_reliability_level(reliability),
        'confidence': 'high' if abs(credibility_score - adjusted_bias) < 0.3 else 'moderate'
    }

def get_reliability_level(score: float) -> str:
    """Get reliability level description"""
    if score >= 0.8:
        return 'highly_reliable'
    elif score >= 0.6:
        return 'reliable'
    elif score >= 0.4:
        return 'questionable'
    else:
        return 'unreliable'

# Additional helper functions for source comparison and research assistance
"""
def perform_comparative_analysis(source_analyses: list) -> dict:
    #Perform comparative analysis across sources
    total_sources = len(source_analyses)
    
    # Analyze credibility distribution
    credibility_scores = [s['credibility']['credibility_score'] for s in source_analyses]
    avg_credibility = sum(credibility_scores) / len(credibility_scores)
    
    # Analyze bias distribution
    bias_scores = [s['bias']['bias_score'] for s in source_analyses]
    avg_bias = sum(bias_scores) / len(bias_scores)
    
    # Find common themes
    all_themes = []
    for source in source_analyses:
        all_themes.extend(source['themes']['content_categories'])
    
    theme_counts = {}
    for theme in all_themes:
        theme_counts[theme] = theme_counts.get(theme, 0) + 1
    
    common_themes = [theme for theme, count in theme_counts.items() if count >= 2]
    
    return {
        'source_count': total_sources,
        'average_credibility': round(avg_credibility, 2),
        'average_bias': round(avg_bias, 2),
        'common_themes': common_themes,
        'credibility_range': f"{min(credibility_scores):.2f} - {max(credibility_scores):.2f}",
        'consensus_level': assess_consensus_level(source_analyses)
    }"""



def suggest_research_sources(topic: str, research_level: str) -> str:
    """
    Suggests research sources for a given topic and level using the Gemini API.

    Args:
        topic: The research topic.
        research_level: The academic level (e.g., 'undergraduate').

    Returns:
        A formatted string of suggested research sources.
    """
    prompt = (
        "As a research librarian, suggest a list of key research sources for the provided topic. "
        "Tailor your suggestions to be appropriate for the specified research level. "
        "Include a mix of academic databases (like JSTOR, PubMed, Scopus), key journals in the field, "
        "foundational books or authors, and reputable online resources or archives. "
        "For each suggestion, provide a brief (1-2 sentence) explanation of why it is relevant."
    )
    context = f"Topic: {topic}\nResearch Level: {research_level}"
    
    # Use the global gemini_chat instance
    response = gemini_chat.chat(prompt, context=context, personality='professor')
    
    if response and response.get('success'):
        return response.get('response', "Could not generate research sources at this time.")
    return "Error: Unable to connect with the research assistant to find sources."

def provide_methodology_guidance(topic: str, research_type: str) -> str:
    """
    Provides guidance on research methodology using the Gemini API.

    Args:
        topic: The research topic.
        research_type: The type of research (e.g., 'empirical', 'literature_review').

    Returns:
        A formatted string containing methodology guidance.
    """
    prompt = (
        "As an academic advisor, provide guidance on appropriate research methodologies for the given topic and research type. "
        "If the type is 'empirical', suggest specific methods like surveys, experiments, case studies, or ethnographic studies. "
        "If 'literature_review', outline the steps for a systematic or narrative review. "
        "If 'theoretical', suggest approaches like conceptual analysis or model building. "
        "Justify why the suggested methodologies are suitable for the topic and research type."
    )
    context = f"Topic: {topic}\nResearch Type: {research_type}"
    
    response = gemini_chat.chat(prompt, context=context, personality='professor')
    
    if response and response.get('success'):
        return response.get('response', "Could not generate methodology guidance at this time.")
    return "Error: Unable to connect with the research assistant for methodology guidance."

def generate_research_questions(topic: str, research_level: str) -> str:
    """
    Generates potential research questions for a topic using the Gemini API.

    Args:
        topic: The research topic.
        research_level: The academic level of the research.

    Returns:
        A formatted string of potential research questions.
    """
    prompt = (
        "As a research supervisor, generate a list of 3-5 potential research questions for the given topic. "
        "The questions should be clear, focused, and arguable. "
        "Ensure the complexity and scope of the questions are appropriate for the specified research level "
        "(e.g., broader for undergraduate, more niche and contributing to a gap in the literature for graduate/professional)."
    )
    context = f"Topic: {topic}\nResearch Level: {research_level}"
    
    response = gemini_chat.chat(prompt, context=context, personality='professor')
    
    if response and response.get('success'):
        return response.get('response', "Could not generate research questions at this time.")
    return "Error: Unable to connect with the research assistant to generate questions."

def create_research_timeline(research_level: str, research_type: str) -> str:
    """
    Creates a generic research project timeline using the Gemini API.

    Args:
        research_level: The academic level (e.g., 'graduate').
        research_type: The type of research (e.g., 'empirical').

    Returns:
        A formatted string representing a research timeline.
    """
    prompt = (
        "As a project manager for academic research, create a structured, generic research timeline. "
        "The timeline should be appropriate for the specified research level and type. "
        "Break the project into key phases (e.g., Preliminary Research, Proposal Development, Data Collection/Analysis, "
        "Drafting, Revision & Submission). Provide estimated durations for each phase (e.g., in weeks or as a percentage of total time). "
        "Acknowledge how the timeline might differ based on the inputs (e.g., an empirical study has a long data collection phase)."
    )
    context = f"Research Level: {research_level}\nResearch Type: {research_type}"
    
    response = gemini_chat.chat(prompt, context=context, personality='professor')
    
    if response and response.get('success'):
        return response.get('response', "Could not generate a research timeline at this time.")
    return "Error: Unable to connect with the research assistant to create a timeline."

def get_research_ethics_guidelines(research_type: str) -> list:
    """Get research ethics guidelines"""
    general_ethics = [
        'Properly cite all sources to avoid plagiarism',
        'Present information accurately and objectively',
        'Acknowledge limitations and potential biases',
        'Respect intellectual property rights'
    ]
    
    if research_type == 'empirical':
        general_ethics.extend([
            'Obtain proper consent for human subjects research',
            'Ensure data privacy and confidentiality',
            'Follow institutional review board guidelines'
        ])
    
    return general_ethics
